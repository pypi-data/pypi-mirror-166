# -*- coding: ascii -*-
"""
aehostd.pam - PAM authentication, authorisation and session handling
"""

import hashlib
import logging
import socket
import secrets

import ldap0
from ldap0.controls.ppolicy import PasswordPolicyControl
import ldap0.dn
import ldap0.filter
from ldap0.controls.sessiontrack import SessionTrackingControl, SESSION_TRACKING_FORMAT_OID_USERNAME
from ldap0.pw import random_string
from ldap0.cache import Cache

import aedir

from .base import BaseThread
#from .base import get_peer_env
from .cfg import CFG
from . import req
from .passwd import PASSWD_NAME_MAP
from .ldapconn import LDAP_CONN
from . import refresh

# PAM request type codes
PAM_REQ_AUTHC = 0x000d0001
PAM_REQ_AUTHZ = 0x000d0002
PAM_REQ_SESS_O = 0x000d0003
PAM_REQ_SESS_C = 0x000d0004
PAM_REQ_PWMOD = 0x000d0005

# PAM result constants
PAM_SUCCESS = 0
PAM_PERM_DENIED = 6
PAM_AUTH_ERR = 7
PAM_CRED_INSUFFICIENT = 8
PAM_AUTHINFO_UNAVAIL = 9
PAM_USER_UNKNOWN = 10
PAM_MAXTRIES = 11
PAM_NEW_AUTHTOK_REQD = 12
PAM_ACCT_EXPIRED = 13
PAM_SESSION_ERR = 14
PAM_AUTHTOK_ERR = 20
PAM_AUTHTOK_DISABLE_AGING = 23
PAM_IGNORE = 25
PAM_ABORT = 26
PAM_AUTHTOK_EXPIRED = 27

# for generating session IDs
SESSION_ID_LENGTH = 25
SESSION_ID_ALPHABET = (
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    'abcdefghijklmnopqrstuvwxyz'
    '01234567890'
)

# random bytes generated at startup
PAM_CACHE_SALT = secrets.token_bytes(16)

# dictionary for caching PAMAuthcReq.process() and PAMAuthzReq.process() results
PAM_CACHE = {
    PAM_REQ_AUTHC: Cache(ttl=CFG.pam_authc_cache_ttl),
    PAM_REQ_AUTHZ: Cache(ttl=CFG.pam_authc_cache_ttl),
}


class PAMCachePurger(BaseThread):
    """
    Thread for purging expired entries from global PAM_CACHE
    """
    __slots__ = (
        '_stop_event',
        '_reset_event',
        '_purge_interval',

    )

    def _run_once(self):
        expired = 0
        for rtype in PAM_CACHE:
            for cache_key in list(PAM_CACHE[rtype]):
                try:
                    PAM_CACHE[rtype][cache_key]
                except KeyError:
                    expired += 1
                    logging.debug('Cached PAM authc result expired and removed')
        if expired:
            logging.info('Expired %d PAM authc result cache item(s)', expired)


class PAMRequest(req.Request):
    """
    base class for handling PAM requests (not directly used)
    """

    def _session_tracking_control(self):
        """
        return SessionTrackingControl instance based on params
        """
        return SessionTrackingControl(
            self._params['rhost'],
            '%s::%s' % (socket.getfqdn(), self._params['service']),
            SESSION_TRACKING_FORMAT_OID_USERNAME,
            self._params.get('ruser', self._params['username']),
        )

    def log_params(self, log_level):
        """
        log request parameters, but mask secret password values
        """
        log_params = dict(self._params)
        for secret_param in ('password', 'oldpassword', 'newpassword'):
            if log_params.get(secret_param):
                log_params[secret_param] = '***'
        self._log(log_level, '(%r)', log_params)

    def fail(self):
        """
        called in case request parameters could not be parsed
        """
        self._msgio.write_int32(self.rtype)
        self._msgio.write_int32(req.RES_BEGIN)
        self._msgio.write_int32(PAM_ABORT)
        self._msgio.write_str('Internal failure')
        self._msgio.write_int32(req.RES_END)


class PAMAuthcReq(PAMRequest):
    """
    handles PAM authc requests
    """

    rtype = PAM_REQ_AUTHC
    msg_format = (
        ('username', str),
        ('service', str),
        ('ruser', str),
        ('rhost', str),
        ('tty', str),
        ('password', str),
    )

    def write(self, result):
        """
        write result to PAM client
        """
        username, authc, authz, msg = result
        self._log(
            (
                logging.WARN
                if authc or authz
                else logging.DEBUG
            ),
            'PAM auth result for %r: authc=%d authz=%d msg=%r',
            username, authc, authz, msg,
        )
        self._msgio.write_int32(req.RES_BEGIN)
        self._msgio.write_int32(authc)
        self._msgio.write_str(username)
        self._msgio.write_int32(authz)
        self._msgio.write_str(msg)
        self._msgio.write_int32(req.RES_END)

    def fail(self):
        """
        called in case request parameters could not be parsed
        """
        self.write((
            '-',
            PAM_ABORT,
            PAM_ABORT,
            'Internal failure',
        ))

    def _cache_key(self):
        key_bytes = repr([
            (key, self._params[key])
            for key in sorted(self._params.keys())
            if key in CFG.pam_authc_cache_attrs
        ]).encode('utf-8')
        chash = hashlib.sha512(PAM_CACHE_SALT)
        chash.update(key_bytes)
        cache_key_digest = chash.hexdigest()
        self._log(logging.DEBUG, '._cache_key() cache_key_digest = %r', cache_key_digest)
        return cache_key_digest

    def _user_dn(self, user_name, search_base):
        """
        construct bind-DN for password check
        """
        if user_name == CFG.aehost_vaccount_t[0]:
            user_dn = CFG.binddn
        else:
            user_dn = 'uid={0},{1}'.format(ldap0.dn.escape_str(user_name), search_base)
        self._log(logging.DEBUG, 'user_dn = %r', user_dn)
        return user_dn

    def process(self):
        """
        handle request, mainly do LDAP simple bind
        """
        user_name = self._params['username']
        if user_name not in PASSWD_NAME_MAP:
            self.write((user_name, PAM_AUTH_ERR, PAM_USER_UNKNOWN, 'Unknown user'))
            return
        # initialize safe result vars
        pam_authc, pam_authz, pam_msg = (PAM_AUTH_ERR, PAM_PERM_DENIED, 'Undefined')
        if CFG.pam_authc_cache_ttl > 0:
            # lookup request result in cache
            cache_key = self._cache_key()
            self._log(logging.DEBUG, 'read cache_key = %r', cache_key)
            try:
                pam_authc, pam_authz, pam_msg = PAM_CACHE[self.rtype][cache_key]
            except KeyError as key_error:
                self._log(
                    logging.DEBUG,
                    'No cached PAM authc result: %r',
                    key_error,
                )
            else:
                self._log(
                    logging.DEBUG,
                    'Return cached PAM authc result: %r',
                    (pam_authc, pam_authz, pam_msg),
                )
                self.write((user_name, pam_authc, pam_authz, pam_msg))
                return
        # bind using the specified credentials
        uris = CFG.get_ldap_uris()
        if LDAP_CONN.current_ldap_uri is not None:
            # if currently connected then try the currently used LDAP server at first
            uris.append(LDAP_CONN.current_ldap_uri)
        self._log(logging.DEBUG, 'Will try simple bind on servers %r', uris)
        try:
            while True:
                ldap_uri = uris.pop()
                self._log(logging.DEBUG, 'Try connecting to %r', ldap_uri)
                try:
                    # open a separate connection
                    conn = aedir.AEDirObject(
                        ldap_uri,
                        trace_level=0,
                        retry_max=0,
                        timeout=CFG.timelimit,
                        cacert_filename=CFG.tls_cacertfile,
                        cache_ttl=0.0,
                    )
                    user_dn = self._user_dn(user_name, LDAP_CONN.search_base or conn.search_base)
                    # verify password by sending simple bind operation
                    bind_res = conn.simple_bind_s(
                        user_dn,
                        self._params['password'],
                        req_ctrls=[
                            PasswordPolicyControl(),
                            self._session_tracking_control(),
                        ],
                    )
                    break
                except ldap0.SERVER_DOWN:
                    if not uris:
                        raise
        except ldap0.INVALID_CREDENTIALS as ldap_err:
            self._log(
                logging.WARN,
                'LDAP simple bind failed to %s as %r: %s',
                conn.uri,
                user_dn,
                ldap_err,
            )
            pam_authc, pam_authz, pam_msg = (
                PAM_AUTH_ERR, PAM_PERM_DENIED, 'Wrong username or password'
            )
            resp_ctrls = ldap_err.ctrls
        else:
            self._log(
                logging.DEBUG,
                'LDAP simple bind successful to %s as %r',
                conn.uri,
                user_dn,
            )
            resp_ctrls = bind_res.ctrls
            if user_name == CFG.aehost_vaccount_t[0]:
                CFG.bindpwfile.write(self._params['password'].encode('utf-8'), mode=0o0640)
                refresh.USERSUPDATER_TASK.reset()
                self.write((user_name, PAM_SUCCESS, PAM_PERM_DENIED, 'Host password check ok'))
                return
            pam_authc, pam_authz, pam_msg = (PAM_SUCCESS, PAM_SUCCESS, 'User password check ok')
            # search password policy response control
        for rctrl in resp_ctrls or []:
            if rctrl.controlType == PasswordPolicyControl.controlType:
                # found a password policy control
                self._log(
                    logging.DEBUG,
                    '%s: error=%r, timeBeforeExpiration=%r, graceAuthNsRemaining=%r',
                    rctrl.__class__.__name__,
                    rctrl.error,
                    rctrl.timeBeforeExpiration,
                    rctrl.graceAuthNsRemaining,
                )
                if rctrl.error == 0:
                    # password is expired but still grace logins
                    pam_authz, pam_msg = (PAM_AUTHTOK_EXPIRED, 'Password expired')
                    if rctrl.graceAuthNsRemaining is not None:
                        pam_authz = PAM_NEW_AUTHTOK_REQD
                        pam_msg += ', %d grace logins left' % (
                            rctrl.graceAuthNsRemaining,
                        )
                elif rctrl.error == 1:
                    pam_authz, pam_msg = (PAM_ACCT_EXPIRED, 'Account is locked')
                elif rctrl.error == 2:
                    pam_authz, pam_msg = (
                        PAM_NEW_AUTHTOK_REQD, 'You must change password after reset'
                    )
                elif rctrl.error is None and rctrl.timeBeforeExpiration is not None:
                    pam_msg = 'Password will expire in %d seconds' % (
                        rctrl.timeBeforeExpiration,
                    )
        if (
                CFG.pam_authc_cache_ttl > 0
                and pam_authc == PAM_SUCCESS
                and pam_authz == PAM_SUCCESS
            ):
            # store result in cache
            self._log(logging.DEBUG, 'store cache_key = %r', cache_key)
            PAM_CACHE[self.rtype].cache(
                cache_key,
                (pam_authc, pam_authz, pam_msg),
                CFG.pam_authc_cache_ttl,
            )
        self.write((user_name, pam_authc, pam_authz, pam_msg))


class PAMAuthzReq(PAMRequest):
    """
    handles PAM authz requests
    """

    rtype = PAM_REQ_AUTHZ
    msg_format = (
        ('username', str),
        ('service', str),
        ('ruser', str),
        ('rhost', str),
        ('tty', str),
    )

    def write(self, result):
        """
        write result to PAM client
        """
        authz, msg = result
        self._msgio.write_int32(req.RES_BEGIN)
        self._msgio.write_int32(authz)
        self._msgio.write_str(msg)
        self._msgio.write_int32(req.RES_END)

    def _check_authz_search(self):
        if not CFG.pam_authz_search:
            return
        # escape all params
        variables = dict((k, ldap0.filter.escape_str(v)) for k, v in self._params.items())
        variables.update(
            hostname=ldap0.filter.escape_str(socket.gethostname()),
            fqdn=ldap0.filter.escape_str(socket.getfqdn()),
            uid=variables['username'],
        )
        filter_tmpl = CFG.pam_authz_search
        if 'rhost' in variables and variables['rhost']:
            filter_tmpl = '(&%s(|(!(aeRemoteHost=*))(aeRemoteHost={rhost})))' % (filter_tmpl)
        ldap_filter = filter_tmpl.format(**variables)
        self._log(logging.DEBUG, 'check authz filter %r', ldap_filter)
        ldap_conn = LDAP_CONN.get_ldap_conn()
        ldap_conn.find_unique_entry(
            ldap_conn.search_base,
            filterstr=ldap_filter,
            attrlist=['1.1'],
            req_ctrls=[self._session_tracking_control()],
        )
        # end of _check_authz_search()

    def process(self):
        """
        handle request, mainly do LDAP authz search
        """
        user_name = self._params['username']
        if user_name not in PASSWD_NAME_MAP:
            self._log(logging.WARN, 'Invalid user name %r', user_name)
            self.write((PAM_PERM_DENIED, 'Invalid user name'))
            return
        if user_name == CFG.aehost_vaccount_t[0]:
            self._log(logging.INFO, 'Reject login with host account %r', user_name)
            self.write((PAM_PERM_DENIED, 'Host account ok, but not authorized for login'))
            return
        # check authorisation search
        try:
            self._check_authz_search()
        except ldap0.LDAPError as ldap_err:
            self._log(logging.WARNING, 'authz failed for %s: %s', user_name, ldap_err)
            self.write((PAM_PERM_DENIED, 'LDAP authz check failed'))
        except (KeyError, ValueError, IndexError) as err:
            self._log(logging.WARNING, 'Value check failed for %s: %s', user_name, err)
            self.write((PAM_PERM_DENIED, 'LDAP authz check failed'))
        else:
            self._log(logging.DEBUG, 'authz ok for %s', user_name)
            # all tests passed, return OK response
            self.write((PAM_SUCCESS, ''))


class PAMPassModReq(PAMRequest):
    """
    handles PAM passmod requests
    """

    rtype = PAM_REQ_PWMOD
    msg_format = (
        ('username', str),
        ('service', str),
        ('ruser', str),
        ('rhost', str),
        ('tty', str),
        ('asroot', int),
        ('oldpassword', str),
        ('newpassword', str),
    )

    def write(self, result):
        """
        write result to PAM client
        """
        code, msg = result
        self._msgio.write_int32(req.RES_BEGIN)
        self._msgio.write_int32(code)
        self._msgio.write_str(msg)
        self._msgio.write_int32(req.RES_END)

    def process(self):
        """
        handle request, just refuse password change
        """
        self.write((PAM_PERM_DENIED, CFG.pam_passmod_deny_msg))


class PAMSessOpenReq(PAMRequest):
    """
    handles PAM session open requests
    """

    rtype = PAM_REQ_SESS_O
    msg_format = (
        ('username', str),
        ('service', str),
        ('ruser', str),
        ('rhost', str),
        ('tty', str),
    )

    def write(self, result):
        """
        write result to PAM client
        """
        self._msgio.write_int32(req.RES_BEGIN)
        # write session from result
        self._msgio.write_str(result)
        self._msgio.write_int32(req.RES_END)

    def process(self):
        """
        handle request, mainly return new generated session id
        """
        session_id = random_string(alphabet=SESSION_ID_ALPHABET, length=SESSION_ID_LENGTH)
        self._log(logging.DEBUG, 'New session ID: %s', session_id)
        self.write(session_id)


class PAMSessCloseReq(PAMRequest):
    """
    handles PAM session close requests
    """

    rtype = PAM_REQ_SESS_C
    msg_format = (
        ('username', str),
        ('service', str),
        ('ruser', str),
        ('rhost', str),
        ('tty', str),
        ('session_id', str),
    )

    def write(self, result):
        """
        write result to PAM client
        """
        self._msgio.write_int32(req.RES_BEGIN)
        self._msgio.write_int32(req.RES_END)

    def process(self):
        """
        handle request, do nothing yet
        """
        self.write(None)
