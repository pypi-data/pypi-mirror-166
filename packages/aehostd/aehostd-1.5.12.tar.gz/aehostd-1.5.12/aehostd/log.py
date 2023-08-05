# -*- coding: ascii -*-
"""
aehostd.log - Logger stuff
"""

import logging
import logging.handlers

from .cfg import CFG


# log format to use when logging to syslog
SYS_LOG_FORMAT = '%(name)s[%(process)d] %(levelname)s %(message)s'

# log format to use when logging to console
CONSOLE_LOG_FORMAT = '%(asctime)s ' + SYS_LOG_FORMAT


def init_logger(log_name, log_level):
    """
    Configure either a global SysLogHandler or StreamHandler logger
    """
    if CFG.logsocket is None:
        # send messages to stderr (console)
        log_format = CONSOLE_LOG_FORMAT
        log_handler = logging.StreamHandler()
    else:
        # send messages to syslog
        log_format = SYS_LOG_FORMAT
        log_handler = logging.handlers.SysLogHandler(
            address=CFG.logsocket or '/dev/log',
            facility=logging.handlers.SysLogHandler.LOG_DAEMON,
        )
    log_handler.setFormatter(logging.Formatter(fmt=log_format))
    logger = logging.getLogger()
    logger.name = log_name
    logger.addHandler(log_handler)
    if log_level is None:
        log_level = logging.INFO
    logger.setLevel(log_level)
