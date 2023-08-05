# -*- coding: ascii -*-
"""
aehostd.ldapconn - maintain LDAP connection
"""

import time
import logging

import ldap0
from ldap0.lock import LDAPLock

from aedir import AEDirObject

from .__about__ import __version__
from .cfg import CFG


def _new_ldap_connection():
    """
    Open new LDAP connection by trying all servers defined in config
    """
    logging.debug('Open new LDAP connection')
    who = cred = None
    if CFG.binddn and CFG.bindpwfile:
        # read password to be used for simple bind
        who = CFG.binddn
        cred = CFG.bindpwfile.read()
    uris = CFG.get_ldap_uris()
    ldap_conn = None
    try_count = 0
    while True:
        try_count += 1
        logging.debug('%d LDAP servers left to try: %s', len(uris), ', '.join(uris))
        if not uris:
            # no more servers left to try
            logging.error(
                'Failed to reach any of %d LDAP servers',
                len(CFG.uri_pool)+len(CFG.uri_list),
            )
            ldap_conn = None
            break
        ldap_uri = uris.pop()
        logging.debug('Try %d. connect to %r ...', try_count, ldap_uri)
        try:
            ldap_conn = AEDirObject(
                ldap_uri,
                trace_level=0,
                retry_max=0,
                timeout=CFG.timelimit,
                who=(
                    None
                    if not cred or ldap_uri.lower().startswith('ldapi://')
                    else who
                ),
                cred=cred,
                cacert_filename=CFG.tls_cacertfile,
                client_cert_filename=CFG.tls_cert,
                client_key_filename=CFG.tls_key,
                cache_ttl=CFG.cache_ttl,
            )
        except (ldap0.LDAPError, AttributeError) as ldap_error:
            ldap_conn = None
            logging.warning(
                'Error connecting to %r: %s',
                ldap_uri,
                ldap_error,
            )
        else:
            if ldap_conn.get_whoami_dn():
                logging.info(
                    'Successfully bound to %r as %r (%r)',
                    ldap_conn.uri,
                    ldap_conn.get_whoami_dn(),
                    id(ldap_conn),
                )
                break
            ldap_conn = None
    return ldap_conn
    # end of _new_connection()


class LDAPConnection:
    """
    class for LDAP connection handling
    """
    __slots__ = (
        '_ldap_conn',
        '_ldap_conn_lock',
        '_ldap_conn_ts',
    )

    def __init__(self):
        # For lazy LDAP connecting in self.get_ldap_conn()
        self._ldap_conn_lock = LDAPLock(
            desc='get_ldap_conn() in {0}'.format(self.__class__.__name__)
        )
        self._ldap_conn = None
        self._ldap_conn_ts = 0.0

    def disable_ldap_conn(self):
        """
        Destroy local LDAPI connection and reset it to None.
        Should be invoked when catching a ldap0.SERVER_DOWN exception.
        """
        try:
            self._ldap_conn_lock.acquire()
            if self._ldap_conn:
                self._ldap_conn.unbind_s()
        finally:
            # Free it
            del self._ldap_conn
            # Reset it
            self._ldap_conn = None
            self._ldap_conn_lock.release()


    @property
    def current_ldap_uri(self):
        """
        property is LDAP URI string if connected, None else
        """
        if isinstance(self._ldap_conn, AEDirObject) and hasattr(self._ldap_conn, '_l'):
            return self._ldap_conn.uri
        return None

    @property
    def search_base(self) -> str:
        """
        property is search_base string if connected, None else
        """
        if isinstance(self._ldap_conn, AEDirObject) and hasattr(self._ldap_conn, '_l'):
            return self._ldap_conn.search_base
        return None

    def get_ldap_conn(self):
        """
        Open a single local LDAP connection and
        bind with locally configured credentials if possible
        """
        current_time = time.time()
        try:
            self._ldap_conn_lock.acquire()
            if (
                    isinstance(self._ldap_conn, AEDirObject)
                    and hasattr(self._ldap_conn, '_l')
                    and self._ldap_conn_ts + CFG.conn_ttl >= current_time
                    and (
                        self._ldap_conn.get_whoami_dn().lower().split(',')[0]
                        == CFG.binddn.lower().split(',')[0]
                    )
                ):
                logging.debug(
                    'Reusing LDAP connection %s to %r',
                    id(self._ldap_conn),
                    self._ldap_conn.uri,
                )
            else:
                # Do not explicitly unbind current connection because
                # it could still be used by another thread
                # => just set to non-functional None and rely on garbage
                #    collection to trigger unbind later
                self._ldap_conn = None
                self._ldap_conn = _new_ldap_connection()
                if self._ldap_conn is None:
                    self._ldap_conn_ts = 0.0
                else:
                    self._ldap_conn_ts = current_time
        finally:
            self._ldap_conn_lock.release()
        return self._ldap_conn


LDAP_CONN = LDAPConnection()
