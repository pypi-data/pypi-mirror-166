# -*- coding: ascii -*-
"""
aehostd.service - Unix domain socket server
"""

import sys
import os
import socket
import socketserver
import time
import logging
import argparse
import threading
import queue
import struct

from lockfile.pidlockfile import PIDLockFile

from .__about__ import __version__
from .cfg import CFG
from .log import init_logger
from .req import MsgIO, get_handlers


SO_PEERCRED_DICT = {
    'linux': (17, '3i'), # for Linux systems
}

# default umask used
UMASK_DEFAULT = 0o0022

# log format to use when logging to syslog
SYS_LOG_FORMAT = '%(levelname)s %(message)s'

# log format to use when logging to console
CONSOLE_LOG_FORMAT = '%(asctime)s %(levelname)s %(message)s'


socket.setdefaulttimeout(CFG.sockettimeout)


def cli_args(script_name, service_desc):
    """
    CLI arguments
    """
    parser = argparse.ArgumentParser(
        prog=script_name,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=service_desc,
    )
    parser.add_argument(
        '-f', '--config',
        dest='cfg_filename',
        default='/etc/aehostd.conf',
        help='configuration file name',
        required=False,
    )
    parser.add_argument(
        '-p', '--pid',
        dest='pidfile',
        default=os.path.join('/', 'var', 'run', 'aehostd', script_name)+'.pid',
        help='PID file name',
        required=False,
    )
    parser.add_argument(
        '-l', '--log-level',
        dest='log_level',
        default=None,
        help='log level',
        type=int,
        required=False,
    )
    parser.add_argument(
        '-n', '--no-fork',
        dest='no_fork',
        default=True,
        help=(
            'Do not fork or daemonise is always set and this '
            'option is only preserved for backward compability.'
        ),
        action='store_true',
        required=False,
    )
    parser.add_argument(
        '-c', '--check',
        dest='check_only',
        default=False,
        help='Check whether demon is running.',
        action='store_true',
        required=False,
    )
    return parser.parse_args()
    # end of cli_args()


def init_service(log_name, service_desc):
    """
    initialize the service instance
    """
    script_name = os.path.basename(sys.argv[0])
    # extract command-line arguments
    args = cli_args(script_name, service_desc)
    # read configuration file
    CFG.read_config(args.cfg_filename)
    init_logger(log_name, args.log_level)
    logging.info(
        'Starting %s %s [%d] reading config %s',
        script_name, __version__,
        os.getpid(),
        args.cfg_filename,
    )
    # log config currently effective options
    for cfg_key in sorted(CFG.__slots__):
        logging.debug('%s = %r', cfg_key, getattr(CFG, cfg_key))
    # clean the environment
    os.environ.clear()
    os.environ['HOME'] = '/'
    os.environ['TMPDIR'] = os.environ['TMP'] = '/tmp'
    os.environ['LDAPNOINIT'] = '1'
    # set log level
    if args.log_level is None:
        logging.getLogger().setLevel(CFG.loglevel)
    # set a default umask for the pidfile and socket
    os.umask(UMASK_DEFAULT)
    # see if someone already locked the pidfile
    pidfile = PIDLockFile(args.pidfile)
    # see if --check option was given
    if args.check_only:
        if pidfile.is_locked():
            logging.debug('pidfile (%s) is locked', args.pidfile)
            sys.exit(0)
        else:
            logging.debug('pidfile (%s) is not locked', args.pidfile)
            sys.exit(1)
    # normal check for pidfile locked
    if pidfile.is_locked():
        logging.error(
            'daemon may already be active, cannot acquire lock (%s)',
            args.pidfile,
        )
        sys.exit(1)
    return script_name, pidfile
    # end of init_service()


class NSSPAMServer(socketserver.UnixStreamServer):
    """
    the NSS/PAM socket server
    """
    timeout = 4.0

    def __init__(self, server_address):
        self.start_time = time.time()
        self._last_mon_time = self.start_time
        self.req_count = 0
        self._last_req_count = 0
        self.req_invalid_count = 0
        self.error_count = 0
        self.bytes_sent_count = 0
        self.avg_response_time = 0
        self.max_response_time = 0
        self.req_threads_active = 0
        self.req_threads_max = 0
        # initialize a map of request handler classes
        self.reqh = {}
        self.reqh.update(get_handlers('aehostd.config'))
        self.reqh.update(get_handlers('aehostd.group'))
        self.reqh.update(get_handlers('aehostd.hosts'))
        self.reqh.update(get_handlers('aehostd.passwd'))
        self.reqh.update(get_handlers('aehostd.pam'))
        # initialize a map of per-request-type request counters
        self.req_counter = {}.fromkeys(self.reqh.keys(), 0)
        self.req_counter_name = {
            rtype: 'req_{}_count'.format(rcls.__name__.lower()[:-3])
            for rtype, rcls in self.reqh.items()
        }
        # initialize queue for incoming requests
        self._request_queue = queue.Queue(maxsize=CFG.threads)
        # set up the threadpool
        self._worker_threads = {}
        for tnum in range(CFG.threads):
            thread_name = '{0}WorkerThread-{1:d}'.format(self.__class__.__name__, tnum)
            thread_instance = threading.Thread(
                target=self.process_request_thread,
                name=thread_name,
                daemon=False,
            )
            thread_instance.enabled = True
            self._worker_threads[thread_name] = thread_instance
            thread_instance.start()
        self.request_queue_size = CFG.qsize
        # Finally start the server and let it accept connections
        socketserver.UnixStreamServer.__init__(
            self,
            server_address,
            None,
            bind_and_activate=True
        )

    @staticmethod
    def _get_peer_cred(request):
        try:
            so_num, struct_fmt = SO_PEERCRED_DICT[sys.platform]
        except KeyError:
            return None, None, None
        peer_creds_struct = request.getsockopt(
            socket.SOL_SOCKET,
            so_num,
            struct.calcsize(struct_fmt)
        )
        pid, uid, gid = struct.unpack(struct_fmt, peer_creds_struct)
        return pid, uid, gid

    def _handle_request(self, request):
        """
        handle a single request
        """
        start_time = time.time()
        handler = None
        try:
            try:
                msgio = MsgIO(request)
                self.req_counter[msgio.rtype] += 1
                handler = self.reqh[msgio.rtype](msgio, self._get_peer_cred(request))
                handler.read_params()
                handler.log_params(logging.DEBUG)
                handler.msgio.write_int32(handler.rtype)
                handler.process()
                response_bytes = handler.msgio.response
                request.sendall(response_bytes)
            except BrokenPipeError:
                handler.log_params(logging.WARNING)
                logging.warning(
                    'Broken pipe sending %s response for request %d',
                    self.reqh[handler.msgio.rtype].__name__,
                    id(request),
                )
            except (KeyboardInterrupt, SystemExit) as exit_err:
                logging.debug(
                    'Received %s exception in %s => re-raise',
                    exit_err,
                    self.__class__.__name__,
                )
                # simply re-raise the exit exception
                raise
            except Exception:
                self.error_count += 1
                if handler is not None:
                    handler.log_params(logging.ERROR)
                    handler.fail()
                    response_bytes = handler.msgio.response
                    request.sendall(response_bytes)
                logging.error(
                    'Unhandled exception during parsing %s[0x%08x] request via %s -> %r',
                    (
                        self.reqh[msgio.rtype].__name__
                        if msgio.rtype in self.reqh
                        else 'unknown'
                    ),
                    msgio.rtype,
                    request.getsockname(),
                    response_bytes,
                    exc_info=True,
                )
            else:
                self.bytes_sent_count += len(response_bytes)
        finally:
            self.shutdown_request(request)
        req_time = 1000 * (time.time() - start_time)
        self.avg_response_time = (self.avg_response_time*30 + req_time) / 31
        self.max_response_time = max(self.max_response_time, req_time)

    def process_request_thread(self):
        """
        This method is passed as argument target when creating Thread instance
        and is invoked by the Thread instance's run() method.
        """
        thread = threading.current_thread()
        thread_info = '%s (PID %s)' % (
            thread.name,
            (
                thread.native_id
                if hasattr(thread, 'native_id')
                else 'unknown'
            ),
        )
        logging.debug('Entering %s', thread_info)
        while self._worker_threads[thread.name].enabled:
            try:
                request = self._request_queue.get(timeout=CFG.socket_select_interval)
            except queue.Empty:
                continue
            logging.debug('%s processing request %d', thread_info, id(request))
            self._handle_request(request)
            self._request_queue.task_done()
        logging.debug('Exiting %s', thread_info)

    def process_request(self, request, client_address):
        """
        Queue new request.
        """
        self.req_count += 1
        logging.debug(
            'Queuing request %d sent by %s',
            id(request),
            request.getsockname(),
        )
        self._request_queue.put(request)

    def get_monitor_data(self):
        """
        returns all monitoring data as
        """
        now = time.time()
        req_all_rate = (self.req_count - self._last_req_count) / (now - self._last_mon_time)
        self._last_mon_time = now
        self._last_req_count = self.req_count
        mon_data = dict(
            req_all_count=self.req_count,
            req_all_rate=req_all_rate,
            req_invalid_count=self.req_invalid_count,
            avg_response_time=self.avg_response_time,
            max_response_time=self.max_response_time,
            bytes_sent_count=self.bytes_sent_count,
            error_count=self.error_count,
            req_threads_active=self.req_threads_active,
            req_threads_max=self.req_threads_max,
            req_qsize=self._request_queue.qsize(),
        )
        mon_data.update({
            self.req_counter_name[rtype]: self.req_counter[rtype]
            for rtype in self.reqh
        })
        return mon_data

    def server_bind(self):
        """
        1. Remove stale socket
        2. Set socket options and permissions
        3. Logging
        """
        try:
            os.unlink(self.server_address)
        except OSError:
            if os.path.exists(self.server_address):
                raise
        self.socket.settimeout(CFG.sockettimeout)
        self.socket.bind(self.server_address)
        self.server_address = self.socket.getsockname()
        os.chmod(self.server_address, int(CFG.socketperms, 8))
        logging.debug(
            '%s bound to %r',
            self.__class__.__name__,
            self.server_address,
        )

    def server_activate(self):
        self.socket.listen(self.request_queue_size)
        logging.debug(
            '%s listens on %r',
            self.__class__.__name__,
            self.server_address,
        )

    def server_close(self):
        for _, thread_instance in self._worker_threads.items():
            thread_instance.enabled = False
        for _, thread_instance in self._worker_threads.items():
            thread_instance.join()
        socketserver.UnixStreamServer.server_close(self)
