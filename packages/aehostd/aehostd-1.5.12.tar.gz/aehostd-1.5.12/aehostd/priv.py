# -*- coding: ascii -*-
"""
aehostd.priv - privileged helper service module
"""

import os
import logging
import time
import shutil

from .__about__ import __version__
from .cfg import CFG
from .service import init_service

LOG_NAME = 'aehostd.priv'

DESCRIPTION = 'Privileged helper service for AE-DIR'

REFRESH_INTERVAL = 2.0


def process_sudoers(last_sudoers_stat):
    """
    Process sudoers file exported by aehostd
    """
    # Fall-back for any error is to retain state
    try:
        sudoers_stat = os.stat(CFG.sudoers_file)
    except OSError:
        # nothing to be done, state unchanged
        return last_sudoers_stat
    next_sudoers_stat = last_sudoers_stat
    if last_sudoers_stat != sudoers_stat:
        target_filename = os.path.join(
            CFG.sudoers_includedir,
            os.path.basename(CFG.sudoers_file),
        )
        logging.debug(
            'New sudoers file at %s to be moved to %s',
            CFG.sudoers_file,
            target_filename,
        )
        try:
            os.chmod(CFG.sudoers_file, 0o440)
            os.chown(CFG.sudoers_file, 0, 0)
            shutil.move(CFG.sudoers_file, target_filename)
        except Exception:
            logging.error(
                'Moving sudoers file at %s to %s failed!',
                CFG.sudoers_file,
                target_filename,
                exc_info=True,
            )
        else:
            logging.info(
                'Successfully moved sudoers file at %s to %s',
                CFG.sudoers_file,
                target_filename,
            )
            next_sudoers_stat = sudoers_stat
    return next_sudoers_stat


def main():
    """
    entry point for privileged helper service running as root
    """
    script_name, ctx = init_service(LOG_NAME, DESCRIPTION)
    # start service
    last_sudoers_stat = None
    with ctx:
        try:
            logging.debug('Started privileged helper service')
            while True:
                if CFG.sudoers_file:
                    last_sudoers_stat = process_sudoers(last_sudoers_stat)
                time.sleep(REFRESH_INTERVAL)
        except (KeyboardInterrupt, SystemExit) as exit_exc:
            logging.debug('Exit exception received: %r', exit_exc)
        logging.info('Stopped %s %s', script_name, __version__)
    # end of main()


if __name__ == '__main__':
    main()
