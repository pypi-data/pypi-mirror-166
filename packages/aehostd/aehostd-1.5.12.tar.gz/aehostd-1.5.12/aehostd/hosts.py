# -*- coding: ascii -*-
"""
aehostd.host - lookup functions for host names and addresses (hosts map)
"""

import logging

from . import req


HOSTS_MAP = {}
HOSTS_NAME_MAP = {}
HOSTS_ADDR_MAP = {}

NSS_REQ_HOST_BYNAME = 0x00050001
NSS_REQ_HOST_BYADDR = 0x00050002
NSS_REQ_HOST_ALL = 0x00050008


def hosts_convert(entry):
    """
    convert an LDAP entry dict to a hosts map tuple
    """
    hostnames = entry['aeFqdn']
    return (hostnames[0], hostnames[1:], entry['ipHostNumber'])


class HostReq(req.Request):
    """
    base class for handling requests to query hosts map
    """

    def write(self, result):
        hostname, aliases, addresses = result
        self._msgio.write_str(hostname)
        self._msgio.write_list(aliases)
        self._msgio.write_int32(len(addresses))
        for address in addresses:
            self._msgio.write_ipaddr(address)


class HostByNameReq(HostReq):
    """
    handle hosts map query for a certain host name
    """

    rtype = NSS_REQ_HOST_BYNAME
    msg_format = (
        ('aeFqdn', str),
    )

    def get_results(self, params):
        try:
            res = hosts_convert(HOSTS_MAP[HOSTS_NAME_MAP[params['aeFqdn']]])
        except KeyError:
            self._log(logging.DEBUG, 'not found %r', params)
            return
        yield res


class HostByAddressReq(HostReq):
    """
    handle hosts map query for a certain address
    """

    rtype = NSS_REQ_HOST_BYADDR
    msg_format = (
        ('ipHostNumber', 'ip'),
    )

    def get_results(self, params):
        try:
            res = hosts_convert(HOSTS_MAP[HOSTS_ADDR_MAP[params['ipHostNumber']]])
        except KeyError:
            self._log(logging.DEBUG, 'not found %r', params)
            return
        yield res


class HostAllReq(HostReq):
    """
    handle hosts map query for a listing all hosts
    """

    rtype = NSS_REQ_HOST_ALL

    def get_results(self, params):
        for _, host_entry in HOSTS_MAP.items():
            yield hosts_convert(host_entry)
