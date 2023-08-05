# -*- coding: ascii -*-
"""
aehostd.group - group entry lookup routines (group map)
"""

import logging

from .cfg import CFG
from . import req

GROUP_MAP = {}
GROUP_NAME_MAP = {}
GROUP_MEMBER_MAP = {CFG.aehost_vaccount_t[0]: []}

NSS_REQ_GROUP_BYNAME = 0x00040001
NSS_REQ_GROUP_BYGID = 0x00040002
NSS_REQ_GROUP_BYMEMBER = 0x00040006
NSS_REQ_GROUP_ALL = 0x00040008


class GroupReq(req.Request):
    """
    base class for handling requests to query group map
    """

    def write(self, result):
        name, passwd, gid, members = result
        self._msgio.write_str(name)
        self._msgio.write_str(passwd)
        self._msgio.write_int32(gid)
        self._msgio.write_list(members)


class GroupByNameReq(GroupReq):
    """
    handle group map query for a certain group name
    """

    rtype = NSS_REQ_GROUP_BYNAME
    msg_format = (
        ('cn', str),
    )

    def get_results(self, params):
        if params['cn'] in CFG.nss_ignore_groups:
            self._log(logging.DEBUG, 'ignore requested group %r', params['cn'])
            return
        try:
            res = GROUP_MAP[GROUP_NAME_MAP[params['cn']]]
        except KeyError:
            self._log(logging.DEBUG, 'not found %r', params)
            return
        yield res


class GroupByGidReq(GroupReq):
    """
    handle group map query for a certain GID
    """

    rtype = NSS_REQ_GROUP_BYGID
    msg_format = (
        ('gidNumber', int),
    )

    def get_results(self, params):
        gid = params['gidNumber']
        if gid < CFG.nss_min_gid or \
           gid > CFG.nss_max_gid or \
           gid in CFG.nss_ignore_gids:
            self._log(logging.DEBUG, 'ignore requested GID %d', gid)
            return
        try:
            res = GROUP_MAP[gid]
        except KeyError:
            self._log(logging.DEBUG, 'not found %r', params)
            return
        yield res


class GroupByMemberReq(GroupReq):
    """
    handle group map query for a certain user name
    """

    rtype = NSS_REQ_GROUP_BYMEMBER
    msg_format = (
        ('memberUid', str),
    )

    def get_results(self, params):
        member_uid = params['memberUid']
        if member_uid in CFG.nss_ignore_users:
            self._log(logging.DEBUG, 'ignore requested memberUid %r', member_uid)
            return
        for gid in GROUP_MEMBER_MAP.get(member_uid, []):
            name, passwd, gid, _ = GROUP_MAP[gid]
            yield (name, passwd, gid, [member_uid])


class GroupAllReq(GroupReq):
    """
    handle group map query for a listing all groups
    """

    rtype = NSS_REQ_GROUP_ALL

    def get_results(self, params):
        for _, group_entry in GROUP_MAP.items():
            yield group_entry
