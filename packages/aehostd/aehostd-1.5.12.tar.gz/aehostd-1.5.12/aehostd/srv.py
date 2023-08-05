# -*- coding: ascii -*-
"""
aehostd.srv - main service module
"""

import logging
import os

from .__about__ import __version__
from .cfg import CFG
from .service import NSSPAMServer, init_service
from . import monitor
from . import refresh
from . import pam
from .refresh import UsersUpdater, NetworkAddrUpdater

LOG_NAME = 'aehostd.srv'

DESCRIPTION = 'NSS/PAM service for AE-DIR'


def main():
    """
    entry point for demon running as non-privileged user
    """
    script_name, ctx = init_service(LOG_NAME, DESCRIPTION)
    # start service
    with ctx:
        try:
            try:
                logging.debug(
                    'Initializing %s instance listening on %r',
                    NSSPAMServer.__name__,
                    CFG.socketpath,
                )
                logging.debug('Start refresh thread')
                # build a list of additional back-group threads
                refresh.USERSUPDATER_TASK = UsersUpdater(CFG.refresh_sleep)
                spawned_threads = [refresh.USERSUPDATER_TASK]
                if CFG.netaddr_refresh > 0 and CFG.netaddr_level > 0:
                    netaddr_refresh_task = NetworkAddrUpdater(CFG.netaddr_refresh)
                    spawned_threads.append(netaddr_refresh_task)
                else:
                    netaddr_refresh_task = None
                if CFG.pam_authc_cache_ttl > 0:
                    spawned_threads.append(pam.PAMCachePurger(CFG.pam_authc_cache_ttl))
                with NSSPAMServer(CFG.socketpath) as server:
                    if CFG.monitor > 0:
                        spawned_threads.append(
                            monitor.Monitor(
                                CFG.monitor,
                                server,
                                refresh.USERSUPDATER_TASK,
                                netaddr_refresh_task,
                            )
                        )
                    # now start the threads
                    for thr in spawned_threads:
                        logging.debug('Starting %s', thr.__class__.__name__)
                        thr.start()
                    logging.info(
                        '%s instance is listening on %r, start serving requests',
                        server.__class__.__name__,
                        server.server_address,
                    )
                    server.serve_forever(poll_interval=CFG.socket_select_interval)
            except (KeyboardInterrupt, SystemExit) as exit_exc:
                logging.debug('Exit exception received: %r', exit_exc)
                for thr in spawned_threads:
                    logging.debug('Stopping %s thread', thr.__class__.__name__)
                    thr.stop()
        finally:
            logging.debug('Removing socket path %r', CFG.socketpath)
            try:
                os.remove(CFG.socketpath)
            except OSError as os_error:
                logging.debug('Error removing socket path %r: %s', CFG.socketpath, os_error)
        logging.info('Stopped %s %s', script_name, __version__)
    # end of main()


if __name__ == '__main__':
    main()
