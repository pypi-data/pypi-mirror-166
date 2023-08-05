# -*- coding: ascii -*-
"""
aehostd.passwd - lookup functions for user account information (passwd map)
"""

import logging

from .cfg import CFG
from . import req


PASSWD_MAP = {}
PASSWD_NAME_MAP = {}

NSS_REQ_PASSWD_BYNAME = 0x00080001
NSS_REQ_PASSWD_BYUID = 0x00080002
NSS_REQ_PASSWD_ALL = 0x00080008


class PasswdReq(req.Request):
    """
    base class for handling requests to query passwd map
    """

    def write(self, result):
        name, passwd, uid, gid, gecos, home, shell = result
        self._msgio.write_str(name)
        self._msgio.write_str(passwd)
        self._msgio.write_int32(uid)
        self._msgio.write_int32(gid)
        self._msgio.write_str(gecos)
        self._msgio.write_str(home)
        self._msgio.write_str(shell)

class PasswdByNameReq(PasswdReq):
    """
    handle passwd map query for a certain user name
    """

    rtype = NSS_REQ_PASSWD_BYNAME
    msg_format = (
        ('uid', str),
    )

    def get_results(self, params):
        username = params['uid']
        if username in CFG.nss_ignore_users:
            self._log(logging.DEBUG, 'ignore requested user %r', username)
            return
        try:
            res = PASSWD_MAP[PASSWD_NAME_MAP[username]]
        except KeyError:
            self._log(logging.DEBUG, 'not found %r', params)
            return
        yield res


class PasswdByUidReq(PasswdReq):
    """
    handle passwd map query for a certain UID
    """

    rtype = NSS_REQ_PASSWD_BYUID
    msg_format = (
        ('uidNumber', int),
    )

    def get_results(self, params):
        userid = params['uidNumber']
        if userid < CFG.nss_min_uid or \
           userid > CFG.nss_max_uid or \
           userid in CFG.nss_ignore_uids:
            self._log(logging.DEBUG, 'ignore requested UID %d', userid)
            return
        try:
            res = PASSWD_MAP[userid]
        except KeyError as err:
            self._log(logging.DEBUG, '%r not found: %s', params, err)
            return
        yield res


class PasswdAllReq(PasswdReq):
    """
    handle passwd map query for a listing all users
    """

    rtype = NSS_REQ_PASSWD_ALL

    def get_results(self, params):
        for _, passwd_entry in PASSWD_MAP.items():
            yield passwd_entry
