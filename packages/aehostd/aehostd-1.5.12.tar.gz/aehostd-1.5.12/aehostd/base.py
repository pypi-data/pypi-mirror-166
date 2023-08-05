# -*- coding: ascii -*-
"""
aehostd.base - very basic stuff
"""

import sys
import os
import logging
import threading


def dict_del(dct, key):
    """
    removes a dictionary element given by `key' but without failing if it
    does not exist
    """
    try:
        del dct[key]
    except KeyError:
        pass


def get_peer_env(
        pid,
        names=('SSH_CLIENT', 'SSH_CONNECTION', 'SSH_TTY'),
    ):
    """
    return dictionary of the process environment vars grabbed from /proc/<pid>
    """
    # FIX ME!
    # This currently only works on Linux because of access to /proc file-system.
    # And it needs to run as root.
    if sys.platform != 'linux':
        logging.debug(
            'Platform is %r => skip reading peer env',
            sys.platform
        )
        return {}
    names = set(names or [])
    peer_env_filename = '/proc/%d/environ' % (pid,)
    try:
        with open(peer_env_filename, 'r', encoding=sys.stdin.encoding) as env_file:
            env_str = env_file.read()
    except IOError as err:
        logging.debug(
            'Error reading peer env from %s: %s',
            peer_env_filename,
            err,
        )
        return {}
    env = {}
    for line in env_str.split('\x00'):
        try:
            name, val = line.split('=', 1)
        except ValueError:
            continue
        if not names or name in names:
            env[name] = val
    logging.debug('Retrieved peer env vars: %r', env)
    return env
    # end of get_peer_env()


class IdempotentFile:
    """
    Class handles a idempotent file on disk
    """

    def __init__(self, path):
        self.path = path

    def __repr__(self):
        return '%s.%s(%r)' % (self.__class__.__module__, self.__class__.__name__, self.path)

    def read(self):
        """
        reads content from file
        """
        try:
            with open(self.path, 'rb') as fileobj:
                content = fileobj.read()
        except (IOError, OSError) as err:
            content = None
            logging.warning('Error reading file %r: %s', self.path, err)
        return content

    def write(self, content, remove=False, mode=0o511):
        """
        writes content to file if needed
        """
        exists = os.path.exists(self.path)
        if exists and content == self.read():
            logging.debug(
                'Content of %r (%d bytes) did not change => skip updating',
                self.path,
                len(content),
            )
            return False
        # if requested remove old file
        if exists and remove:
            try:
                os.remove(self.path)
            except OSError:
                pass
        # actually write new content to file
        try:
            with os.fdopen(
                    os.open(self.path, os.O_CREAT|os.O_WRONLY, mode=mode),
                    'wb',
                ) as fileobj:
                fileobj.write(content)
        except (IOError, OSError) as err:
            updated = False
            logging.error(
                'Error writing content to file %r: %s',
                self.path,
                err,
            )
        else:
            updated = True
            logging.info('Wrote new content (%d bytes) to file %r', len(content), self.path)
        return updated


class BaseThread(threading.Thread):
    """
    base class for all threads
    """
    __slots__ = (
        '_interval',
        '_stop_event',
        '_reset_event',
    )

    def __init__(self, interval):
        self._interval = interval
        self._stop_event = threading.Event()
        self._reset_event = threading.Event()
        threading.Thread.__init__(
            self,
            group=None,
            target=None,
            name=None,
            args=(),
            kwargs={}
        )

    def _run_once(self):
        """
        run the worker job
        """

    def stop(self):
        """
        stop the thread via stop event
        """
        self._reset_event.set()
        self._stop_event.set()

    def run(self):
        """
        run forever until stop event is set
        """
        logging.debug('Starting %s.run()', self.__class__.__name__)
        while not self._stop_event.is_set():
            logging.debug('Invoking %s._run_once()', self.__class__.__name__)
            self._run_once()
            self._reset_event.wait(self._interval)
        logging.debug('Exiting %s.run()', self.__class__.__name__)
