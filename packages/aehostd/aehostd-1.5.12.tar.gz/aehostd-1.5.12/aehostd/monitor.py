# -*- coding: ascii -*-
"""
aehostd.monitor - write monitor data
"""

import logging

from .base import BaseThread


def key_value_monitor_output(data: dict) -> str:
    """
    returns string representing data to be logged as monitor output
    """
    return ' '.join([
        '{0}={1}'.format(key, val)
        for key, val in data.items()
    ])


class Monitor(BaseThread):
    """
    monitoring thread
    """

    def __init__(self, monitor_interval, server, user_refresh, netaddr_refresh):
        BaseThread.__init__(self, monitor_interval)
        self._server = server
        self._user_refresh = user_refresh
        self._netaddr_refresh = netaddr_refresh

    def _log(self, log_level, msg, *args, **kwargs):
        """
        log one line prefixed with class name
        """
        msg = ' '.join((self.__class__.__name__, msg))
        logging.log(log_level, msg, *args, **kwargs)

    def _run_once(self):
        self._log(
            logging.INFO,
            '%s %s',
            self._server.__class__.__name__,
            key_value_monitor_output(self._server.get_monitor_data()),
        )
        self._log(
            logging.INFO,
            '%s %s',
            self._user_refresh.__class__.__name__,
            key_value_monitor_output(self._user_refresh.get_monitor_data()),
        )
        if self._netaddr_refresh is not None:
            self._log(
                logging.INFO,
                '%s %s',
                self._netaddr_refresh.__class__.__name__,
                key_value_monitor_output(self._netaddr_refresh.get_monitor_data()),
            )
