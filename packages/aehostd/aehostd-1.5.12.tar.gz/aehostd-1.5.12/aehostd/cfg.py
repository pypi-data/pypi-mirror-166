# -*- coding: ascii -*-
"""
aehostd.cfg - configuration vars
"""

import os
import socket
import pwd
import grp
import logging
from configparser import ConfigParser
import collections

from .base import IdempotentFile


# name of default section in .ini file
DEFAULT_SECTION = 'aehostd'


def val_list(cfg_val):
    """
    Returns list of values splitted from space- or comma-separated string
    with all white-spaces stripped
    """
    vset = set()
    res = []
    for val in (cfg_val or '').strip().replace(',', '\n').replace(' ', '\n').split('\n'):
        val = val.strip()
        if val and val not in vset:
            res.append(val)
            vset.add(val)
    return res


def val_set(cfg_val):
    """
    Returns set of values splitted from space- or comma-separated string
    with all white-spaces stripped
    """
    return set(val_list(cfg_val))


def rotated_val_list(cfg_val, rval=None):
    """
    Returns list of values splitted by val_list() rotated by rval.
    """
    if not cfg_val:
        return []
    lst = collections.deque(sorted(val_list(cfg_val)))
    if rval is None:
        rval = hash(socket.getfqdn()) % len(lst)
    lst.rotate(rval)
    return lst


class ConfigParameters:
    """
    method-less class containing all config params
    """
    __slots__ = (
        'aehost_vaccount',
        'aehost_vaccount_t',
        'binddn',
        'bindpwfile',
        'cache_ttl',
        'conn_ttl',
        'cvtsudoers_exec',
        'gecos_tmpl',
        'gid',
        'homedir_tmpl',
        'loginshell_default',
        'loginshell_override',
        'loglevel',
        'logsocket',
        'monitor',
        'netaddr_level',
        'netaddr_refresh',
        'nss_ignore_gids',
        'nss_ignore_groups',
        'nss_ignore_uids',
        'nss_ignore_users',
        'nss_max_gid',
        'nss_max_uid',
        'nss_min_gid',
        'nss_min_uid',
        'pam_authc_cache_attrs',
        'pam_authc_cache_ttl',
        'pam_authz_search',
        'pam_passmod_deny_msg',
        'qsize',
        'refresh_sleep',
        'socketpath',
        'socketperms',
        'sockettimeout',
        'sshkeys_dir',
        'socket_select_interval',
        'sudoers_file',
        'sudoers_includedir',
        'threads',
        'timelimit',
        'tls_cacertfile',
        'tls_cert',
        'tls_key',
        'uid',
        'uid',
        'uri_list',
        'uri_pool',
        'vgroup_gid2attr',
        'vgroup_name2attr',
        'vgroup_name_prefix',
        'vgroup_rgid_offset',
        'vgroup_role_map',
        'visudo_exec',
    )
    cfg_type_map = {
        'monitor': float,
        'refresh_sleep': float,
        'search_timelimit': float,
        'cache_ttl': float,
        'conn_ttl': float,
        'loglevel': int,
        'netaddr_level': int,
        'netaddr_refresh': float,
        'nss_max_gid': int,
        'nss_max_uid': int,
        'nss_min_gid': int,
        'nss_min_uid': int,
        'uri_list': val_list,
        'uri_pool': rotated_val_list,
        'socket_select_interval': float,
        'sockettimeout': float,
        'timelimit': float,
        'vgroup_rgid_offset': int,
        'bindpwfile': IdempotentFile,
        'pam_authc_cache_attrs': val_set,
        'pam_authc_cache_ttl': float,
        'threads': int,
    }

    def __init__(self):

        # General process parameters
        #-------------------------------------------
        # the user name or ID aehostd should be run as
        # ignored since version 1.2.0
        self.uid = None
        # the group name or ID aehostd should be run as
        # ignored since version 1.2.0
        self.gid = None
        # number of NSS/PAM handler threads to start
        self.threads = 4
        # size of request queue
        self.qsize = 10 * self.threads

        # Parameters for logging and monitoring
        #-------------------------------------------
        # Level of log details (int), see Python's standard logging module
        self.loglevel = logging.INFO
        # Path name of syslog socket:
        # Setting this to a string enforces using syslog, empty string results
        # in default syslog socket /dev/log being used.
        # None sends log messages to stderr
        self.logsocket = None
        # Interval (seconds) at which internal monitoring data is written to log.
        # Setting this to zero or negative value disables monitor logging completely.
        self.monitor = -1.0

        # Parameters for the Unix domain socket over which
        # to receive requests from front-end modules
        #-------------------------------------------------
        # Path name of service socket which must match what PAM and NSS modules expect
        self.socketpath = '/var/run/aehostd/socket'
        # timeout of service socket
        self.sockettimeout = 10.0
        # permissions set for service socket
        self.socketperms = '0666'
        # Select timeout in socket server (seconds)
        self.socket_select_interval = 1.0

        # LDAP connection parameters
        #-------------------------------------------
        # At least one of uri_list or uri_pool must be specified.
        # Both uri_list or uri_pool may be specified.
        # List of LDAP servers (LDAP URIs) to try first in exactly this order
        # no matter what is configured in uri_pool.
        self.uri_list = []
        # List of LDAP servers (LDAP URIs) to try after all LDAP URIs defined with uri_list failed.
        # This list gets rotated based on hosts's canonical FQDN for client-side load-balancing.
        self.uri_pool = []
        # The bind-DN to use when binding as service to AE-DIR with simple bind.
        # Preferrably the short bind-DN should be used.
        self.binddn = None
        # The password file to use for simple bind as identity given in binddn.
        self.bindpwfile = IdempotentFile('/var/lib/aehostd/aehostd.pw')
        # Timeout (seconds) used for all LDAP connections/operations
        self.timelimit = 6.0
        # LDAPObject cache TTL used for short-time LDAP search cache.
        self.cache_ttl = 6.0
        # File containing trusted root CA certificate(s).
        # If None the system-wide trust store is used.
        self.tls_cacertfile = None
        # File containing client certificate used for SASL/EXTERNAL bind.
        self.tls_cert = None
        # File containing private key used for SASL/EXTERNAL bind.
        self.tls_key = None
        # Time span (seconds) after which aehostd forcibly reconnects.
        self.conn_ttl = 1800.0

        # NSS map parameters
        #-------------------------------------------
        # Names of passwd entries to ignore
        # Default: All user names found in local file /etc/passwd
        self.nss_ignore_users = {x.pw_name for x in pwd.getpwall()}
        # IDs of passwd entries to ignore
        # Default: All UIDs found in local file /etc/passwd
        self.nss_ignore_uids = {x.pw_uid for x in pwd.getpwall()}
        # Names of group entries to ignore
        # Default: All user names found in local file /etc/group
        self.nss_ignore_groups = {x.gr_name for x in grp.getgrall()}
        # IDs of group entries to ignore
        # Default: All UIDs found in local file /etc/group
        self.nss_ignore_gids = {x.pw_gid for x in pwd.getpwall()}
        # Refresh time (seconds) for NSS passwd and group maps
        self.refresh_sleep = 60.0

        # Minimum numeric UID to handle in passwd requests
        self.nss_min_uid = 0
        # Minimum numeric GID to handle in group requests
        self.nss_min_gid = 0
        # Maximum numeric UID to handle in passwd requests
        self.nss_max_uid = 65500
        # Maximum numeric GID to handle in group requests
        self.nss_max_gid = 65500

        # Refresh time (seconds) for hosts maps.
        # Negative values disables hosts refresh.
        self.netaddr_refresh = -1.0
        # Levels (int) to go up for deriving the hosts map search base.
        self.netaddr_level = 2

        # Name prefix used for virtual groups
        self.vgroup_name_prefix = 'ae-vgrp-'
        # Number offset (int) to be used for virtual groups
        self.vgroup_rgid_offset = 9000

        # Directory name where to store exported SSH authorized keys
        # Setting this to None disables retrieving SSH authorized keys
        self.sshkeys_dir = None

        # passwd string of virtual user account used to authenticate as own aeHost object
        self.aehost_vaccount = (
            'aehost-init:x:9042:9042:AE-DIR virtual host init account:/tmp:/usr/sbin/nologin'
        )
        # Template string for deriving GECOS field from e.g. user name
        self.gecos_tmpl = 'AE-DIR user {username}'
        # Template string for deriving home directory path name from e.g. user name
        # Field names which can be used in template string:
        # - username,
        # - uid (for numeric POSIX-UID)
        # - gid (for numeric POSIX-GID)
        self.homedir_tmpl = None
        # Login shell to be used if attribute loginShell is not available
        self.loginshell_default = '/usr/sbin/nologin'
        # Login shell always used not matter what's in attribute loginShell
        self.loginshell_override = None

        # sudo parameters
        #-------------------------------------------
        # Path name of sudoers export file to be picked up by privileged helper
        self.sudoers_file = '/var/lib/aehostd/ae-dir-sudoers-export'
        # Directory name where privileged helper stores sudoers export file
        self.sudoers_includedir = '/etc/sudoers.d'
        # pathname of visudo executable
        self.visudo_exec = '/usr/sbin/visudo'
        # pathname of visudo cvtsudoers
        self.cvtsudoers_exec = '/usr/bin/cvtsudoers'

        # PAM parameters
        #-------------------------------------------
        # LDAP filter template used for checking authorization of a user
        self.pam_authz_search = None
        # Error message sent to user about password change disabled/denied
        self.pam_passmod_deny_msg = None
        # PAM request attributes to be used for caching of PAM authc results
        self.pam_authc_cache_attrs = {
            'username',
            'password',
        }
        # Cache TTL (seconds) of PAM authc results
        # Setting this to negative value disables caching
        self.pam_authc_cache_ttl = -1.0

        # this is not a config parameter
        self.aehost_vaccount_t = self._passwd_tuple(self.aehost_vaccount)

        # to make pylint happy
        self.vgroup_role_map = self.vgroup_gid2attr = self.vgroup_name2attr = None


    @staticmethod
    def _passwd_tuple(pw_str):
        """
        split passwd line into tuple
        """
        passwd_fields = pw_str.split(':')
        return (
            passwd_fields[0],
            passwd_fields[1],
            int(passwd_fields[2]),
            int(passwd_fields[3]),
            passwd_fields[4],
            passwd_fields[5],
            passwd_fields[6],
        )

    def get_ldap_uris(self):
        """
        return combined list of LDAP URIs to connect to
        derived from config parameters 'uri_pool' and 'uri_list'
        """
        return list(self.uri_pool)[:] + list(reversed(self.uri_list))

    def read_config(self, cfg_filename):
        """
        read and parse config file into dict
        """
        if not os.path.exists(cfg_filename):
            raise SystemExit('Configuration file %r is missing!' % (cfg_filename))
        cfg_parser = ConfigParser(
            interpolation=None,
            default_section=DEFAULT_SECTION,
        )
        cfg_parser.read([cfg_filename])
        for key in sorted(cfg_parser.defaults()):
            if not hasattr(self, key):
                raise ValueError('Unknown config key-word %r' % (key))
            type_func = self.cfg_type_map.get(key, str)
            raw_val = cfg_parser.get(DEFAULT_SECTION, key)
            try:
                val = type_func(raw_val)
            except ValueError as val_err:
                raise ValueError(
                    'Invalid value for %r. Expected %s string, but got %r' % (
                        key,
                        type_func.__name__,
                        raw_val,
                    )
                ) from val_err
            setattr(CFG, key, val)
        # compose parameters for virtual groups
        self.vgroup_role_map = {
            tpl[0]: (
                self.vgroup_rgid_offset+ind,
                ''.join((self.vgroup_name_prefix, 'role-', tpl[1]))
            )
            for ind, tpl in enumerate((
                ('aeVisibleGroups', 'all'),
                ('aeLoginGroups', 'login'),
                ('aeLogStoreGroups', 'log'),
                ('aeSetupGroups', 'setup'),
                ('aeDisplayNameGroups', 'dname'),
            ))
        }
        self.vgroup_gid2attr = {
            val[0]: attr
            for attr, val in self.vgroup_role_map.items()
        }
        self.vgroup_name2attr = {
            val[1]: attr
            for attr, val in self.vgroup_role_map.items()
        }
        # some more user config parameters
        self.aehost_vaccount_t = self._passwd_tuple(self.aehost_vaccount)
        # at least one worker-thread used
        self.threads = max(1, self.threads)
        # end of read_config()


CFG = ConfigParameters()
