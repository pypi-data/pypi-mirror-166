# -*- coding: ascii -*-
"""
aehostd.refresh - various worker threads for data refreshing
"""

import os
import glob
import time
import logging
import pprint
import random
import subprocess
from io import BytesIO

import ldap0
from ldap0.dn import DNObj
from ldap0.ldif import LDIFWriter
from ldap0.functions import strf_secs
from ldap0.controls.deref import DereferenceControl

from .base import BaseThread, IdempotentFile, dict_del
from .cfg import CFG
from . import passwd
from . import group
from . import hosts
from .ldapconn import LDAP_CONN


SUDOERS_ATTRS = [
    'cn',
    'objectClass',
    'sudoCommand',
    'sudoHost',
    'sudoNotAfter', 'sudoNotBefore',
    'sudoOption', 'sudoOrder',
    'sudoRunAs', 'sudoRunAsGroup', 'sudoRunAsUser', 'sudoUser',
]


class RefreshThread(BaseThread):
    """
    Update thread for retrieving SSH authorized keys and sudoers entries

    Thread is initialized by NSSPAMServer, started by main script
    """
    __slots__ = (
        '_last_run',
        '_rand',
        '_rand_factor',
        '_refresh_sleep',
        '_stop_event',
        'avg_refresh_time',
        'max_refresh_time',
        'refresh_counter',
    )
    avg_window = 30.0

    def __init__(self, refresh_sleep):
        BaseThread.__init__(self, refresh_sleep)
        self._rand = random.SystemRandom()
        self._rand_factor = self._interval * 0.06
        self.refresh_counter = 0
        self.avg_refresh_time = 0.0
        self.max_refresh_time = 0.0
        self._last_run = 0.0
        self.reset()

    def _log(self, log_level, msg, *args, **kwargs):
        msg = ': '.join((self.__class__.__name__, msg))
        logging.log(log_level, msg, *args, **kwargs)

    def _refresh_task(self, ldap_conn):
        """
        refresh task
        """
        raise NotImplementedError

    def get_monitor_data(self):
        """
        returns all monitoring data as dict
        """
        return dict(
            refresh_count=self.refresh_counter,
            avg_refresh_time=self.avg_refresh_time,
            max_refresh_time=self.max_refresh_time,
        )

    def reset(self):
        """
        trigger next run, skips refresh sleep time
        """
        # simply reset run timestamps
        self._reset_event.set()
        self._log(logging.INFO, 'Finished %s.reset()', self.__class__.__name__)

    def run(self):
        """
        retrieve data forever
        """
        self._log(logging.DEBUG, 'Starting %s.run()', self.__class__.__name__)
        while not self._stop_event.is_set():
            if not self._reset_event.is_set():
                # wait for refresh time interval plus random jitter
                wait_time = self._interval + self._rand_factor * self._rand.random()
                self._log(logging.DEBUG, 'wait for %0.2f secs', wait_time)
                self._reset_event.wait(wait_time)
            self._reset_event.clear()
            if self._stop_event.is_set():
                # if stop-event was set in the mean-time we exit immediately
                break
            start_time = time.time()
            self._log(logging.DEBUG, 'Invoking %s._refresh_task()', self.__class__.__name__)
            try:
                ldap_conn = LDAP_CONN.get_ldap_conn()
                if ldap_conn is None:
                    self._log(
                        logging.WARN,
                        'No valid LDAP connection => abort',
                    )
                else:
                    self._refresh_task(ldap_conn)
                    self.refresh_counter += 1
                    refresh_time = time.time() - start_time
                    self.max_refresh_time = max(self.max_refresh_time, refresh_time)
                    avg_window = min(self.avg_window, self.refresh_counter)
                    self.avg_refresh_time = (
                        ((avg_window - 1) * self.avg_refresh_time + refresh_time) / avg_window
                    )
                    self._log(
                        logging.INFO,
                        '%d. refresh run with %s (%0.3f secs, avg: %0.3f secs)',
                        self.refresh_counter,
                        ldap_conn.uri,
                        refresh_time,
                        self.avg_refresh_time,
                    )
            except ldap0.SERVER_DOWN as ldap_error:
                self._log(
                    logging.WARN,
                    'Invalid connection: %s',
                    ldap_error,
                )
                LDAP_CONN.disable_ldap_conn()
            except Exception:
                self._log(
                    logging.ERROR,
                    'Aborted refresh with unhandled exception',
                    exc_info=True,
                )
            self._last_run = start_time
        self._log(logging.DEBUG, 'Exiting %s.run()', self.__class__.__name__)


def visudo_check_cmd(sudoers_filename):
    """
    return command arguments for running visudo to check the given file
    """
    return [CFG.visudo_exec, '-c', '-s', '-q', '-f', sudoers_filename]


class UsersUpdater(RefreshThread):
    """
    Thread spawned to update user and group map caches
    """
    __slots__ = (
        '_highest_aegroup_timestamp',
        '_last_role_groups',
    )
    posix_account_attrs = [
        'aeRemoteHost',
        'uidNumber',
        'sshPublicKey',
    ]

    def __init__(self, refresh_sleep):
        RefreshThread.__init__(self, refresh_sleep)
        self._highest_aegroup_timestamp = strf_secs(0.0)
        self._last_role_groups = None
        # at this time CFG.aehost_vaccount_t is ready,
        # so let's first initialize global passwd map here
        passwd.PASSWD_MAP.update({CFG.aehost_vaccount_t[2]: CFG.aehost_vaccount_t})
        passwd.PASSWD_NAME_MAP.update({CFG.aehost_vaccount_t[0]: CFG.aehost_vaccount_t[2]})
        group.GROUP_MEMBER_MAP = {CFG.aehost_vaccount_t[0]: []}
        if CFG.homedir_tmpl is None:
            self.posix_account_attrs.append('homeDirectory')
        if CFG.loginshell_override is None:
            self.posix_account_attrs.append('loginShell')
        self.srvgrp_deref_ctrl = DereferenceControl(
            True,
            {
                'aeVisibleGroups': ['gidNumber', 'memberUid', 'modifyTimestamp'],
                'aeVisibleSudoers': SUDOERS_ATTRS,
            }
        )
        # stuff for sudoers
        if CFG.sudoers_file:
            self.ldif_filename = CFG.sudoers_file+'.ldif'
            self.sudoers_tmp_filename = CFG.sudoers_file+'.tmp'
            self.cvtsudoers_cmd = [
                CFG.cvtsudoers_exec,
                '-d', 'all',
                '-i', 'LDIF',
                '-f', 'sudoers',
                '-o', self.sudoers_tmp_filename,
                self.ldif_filename,
            ]
            self.visudo_check_cmd = visudo_check_cmd(self.sudoers_tmp_filename)

    @staticmethod
    def _passwd_convert(entry):
        """
        convert an LDAP entry dict to a passwd map tuple
        """
        name = entry['uid'][0]
        uid = int(entry['uidNumber'][0])
        # primary GID as UID in case of unique primary user GIDs
        gid = uid
        gecos = entry.get(
            'cn',
            [CFG.gecos_tmpl.format(username=name)]
        )[0]
        if CFG.homedir_tmpl:
            home = CFG.homedir_tmpl.format(username=name, uid=uid, gid=gid)
        else:
            home = entry['homeDirectory'][0]
        if CFG.loginshell_override is None:
            shell = entry.get('loginShell', [CFG.loginshell_default])[0]
        else:
            shell = CFG.loginshell_override
        return (name, 'x', uid, gid, gecos, home, shell)
        # end of UsersUpdater._passwd_convert()

    @staticmethod
    def _group_convert(entry):
        """
        convert an LDAP entry dict to a group map tuple
        """
        logging.debug('group_convert(): %r', entry)
        return (
            entry['cn'][0],
            'x',
            int(entry['gidNumber'][0]),
            entry.get('memberUid', tuple()),
        )
        # end of UsersUpdater._group_convert()

    def _store_ssh_key(self, user):
        user_entry = user.entry_s
        user_name = user_entry['uid'][0]
        self._log(
            logging.DEBUG,
            'Found user %r with %d SSH keys',
            user_name,
            len(user_entry['sshPublicKey']),
        )
        raddr_list = [
            av.strip()
            for av in user_entry.get('aeRemoteHost', [])
            if av.strip()
        ]
        if raddr_list:
            self._log(logging.DEBUG, 'Attribute aeRemoteHost contains: %r', raddr_list)
            ssh_key_prefix = 'from="%s" ' % (','.join(raddr_list))
        else:
            ssh_key_prefix = ''
        self._log(logging.DEBUG, 'ssh_key_prefix = %r', ssh_key_prefix)
        new_user_ssh_keys = sorted([
            ''.join((ssh_key_prefix, ssh_key.strip()))
            for ssh_key in user_entry['sshPublicKey']
        ])
        sshkey_file = IdempotentFile(os.path.join(CFG.sshkeys_dir, user_name))
        sshkey_file.write('\n'.join(new_user_ssh_keys).encode('utf-8'), mode=0o0640)
        # end of store_ssh_key()

    def _export_sudoers(self, sudoers_results, role_groups):
        """
        write sudoers entries to LDIF file and convert it
        """
        if not CFG.sudoers_file:
            self._log(logging.DEBUG, 'sudoers_file undefined => skip sudoers export')
            return
        # extract set of groups valid to be used in sudoUser attribute
        sudoers_groups = {
            group_name[3:].split(',', 1)[0].encode('utf-8')
            for group_name in role_groups['aeLoginGroups']
        }
        self._log(logging.DEBUG, 'Valid sudoers groups set: %r', sudoers_groups)
        # generate LDIF data in memory, filtering out invalid sudoUser values
        ldif_file = BytesIO()
        ldif_writer = LDIFWriter(ldif_file)
        for res in sudoers_results:
            res.entry_b[b'sudoUser'] = [
                sudo_user
                for sudo_user in res.entry_b[b'sudoUser']
                if sudo_user[1:] in sudoers_groups
            ]
            if res.entry_b[b'sudoUser']:
                self._log(logging.DEBUG, 'Added sudoers entry %r: %r', res.dn_s, res.entry_s)
                ldif_writer.unparse(res.dn_b, res.entry_b)
            else:
                self._log(logging.WARN, 'Skipped sudoers entry %r: %r', res.dn_s, res.entry_s)
        ldif_str = ldif_file.getvalue()
        # write LDIF data to file
        ldif_file = IdempotentFile(self.ldif_filename)
        if not ldif_file.write(ldif_str, mode=0o0640, remove=True):
            return
        if not os.path.exists(self.ldif_filename):
            self._log(
                logging.ERROR,
                'LDIF sudoers file %r does not exist!',
                self.ldif_filename,
            )
            return
        # Use cvssudoers to convert LDIF to sudoers file
        self._log(
            logging.DEBUG,
            'Converting LDIF to sudoers file: %r',
            self.cvtsudoers_cmd,
        )
        cvssudoers_rc = subprocess.call(self.cvtsudoers_cmd, shell=False)
        if cvssudoers_rc != 0:
            self._log(
                logging.ERROR,
                'Converting to sudoers file %r failed with return code %d, command was: %r',
                self.sudoers_tmp_filename,
                cvssudoers_rc,
                self.cvtsudoers_cmd,
            )
            return
        # Check syntax of sudoers file with visudo
        self._log(
            logging.DEBUG,
            'Checking sudoers file: %r',
            self.visudo_check_cmd,
        )
        visudo_rc = subprocess.call(self.visudo_check_cmd, shell=False)
        if visudo_rc != 0:
            self._log(
                logging.ERROR,
                'Checking sudoers file %r failed with return code %d, command was: %r',
                self.sudoers_tmp_filename,
                visudo_rc,
                self.visudo_check_cmd,
            )
            return
        os.chmod(self.sudoers_tmp_filename, 0o440)
        os.rename(self.sudoers_tmp_filename, CFG.sudoers_file)
        self._log(
            logging.INFO,
            'Successfully updated sudoers file %s with %d entries',
            CFG.sudoers_file,
            ldif_writer.records_written,
        )
        # end of _export_sudoers()

    def _check_group_timestamps(self, group_results):
        """
        determine whether to trigger full user refresh by looking at most recent
        modifyTimestamp of all user group entries
        """
        highest_group_timestamp = max([
            group_res.entry_s['modifyTimestamp'][0]
            for group_res in group_results
        ])
        self._log(logging.DEBUG, 'highest_group_timestamp = %r', highest_group_timestamp)
        if highest_group_timestamp > self._highest_aegroup_timestamp:
            self._log(
                logging.DEBUG,
                'At least one group entry changed since last run (%s > %s) '
                '=> force full user refresh',
                highest_group_timestamp,
                self._highest_aegroup_timestamp,
            )
            self._reset_last_groups()
            self._highest_aegroup_timestamp = highest_group_timestamp

    def _group_membership_map(self, group_map, passwd_name_map):
        """
        build the user-to-group-membership dict
        """
        group_member_map = {CFG.aehost_vaccount_t[0]: set()}
        for group_map_entry in group_map.values():
            gid_number = group_map_entry[2]
            for user_name in group_map_entry[3]:
                if user_name not in passwd_name_map:
                    continue
                try:
                    group_member_map[user_name].add(gid_number)
                except KeyError:
                    group_member_map[user_name] = set([gid_number])
        return group_member_map

    def _get_group_maps(self, ldap_conn):
        """
        initialize group map and search LDAP groups
        """
        role_groups = {
            role_attr: set()
            for role_attr in CFG.vgroup_role_map
        }
        # init group map dictionaries
        group_map = {}
        group_name_map = {}
        group_dn2id_map = {}
        for group_id, group_name in CFG.vgroup_role_map.values():
            group_map[group_id] = UsersUpdater._group_convert({
                'cn': [group_name],
                'gidNumber': [group_id],
                'memberUid': set(),
            })
            group_name_map[group_name] = group_id
        # First provoke a noSuchObject error in case aeHost entry was moved
        try:
            res_iter = ldap_conn.get_service_groups(
                ldap_conn.get_whoami_dn(),
                attrlist=CFG.vgroup_role_map.keys(),
                req_ctrls=[self.srvgrp_deref_ctrl],
            )
        except ldap0.NO_SUCH_OBJECT as ldap_err:
            # likely own entry could not be read
            # => assume we're not yet initialized or replica not up-to-date
            self._log(logging.WARNING, 'LDAP result noSuchObject triggers re-bind: %s', ldap_err)
            self.reset()
            raise ldap0.SERVER_DOWN('forced re-bind')
        # query the service groups including dereferenced group entries
        group_results = []
        sudoers_results = []
        for res in res_iter:
            for srvgrp in res.rdata:
                self._log(
                    logging.DEBUG,
                    'Extracting aeVisibleGroups and aeVisibleSudoers from %s',
                    srvgrp.dn_s,
                )
                for role_attr in CFG.vgroup_role_map:
                    role_groups[role_attr].update(srvgrp.entry_s.get(role_attr, []))
                for ctrl in srvgrp.ctrls:
                    if ctrl.controlType == DereferenceControl.controlType:
                        group_results.extend([
                            grp
                            for grp in ctrl.derefRes.get('aeVisibleGroups', [])
                            if grp.entry_b
                        ])
                        sudoers_results.extend([
                            sre
                            for sre in ctrl.derefRes.get('aeVisibleSudoers', [])
                            if sre.entry_b
                        ])
        # build and convert complete group entry
        all_user_names = set()
        for group_res in group_results:
            self._log(logging.DEBUG, 'LDAP group entry %r : %r', group_res.dn_s, group_res.entry_s)
            # extract group name from entry DN
            group_name = group_res.dn_s.split(',', 1)[0][3:]
            gid_number = int(group_res.entry_s['gidNumber'][0])
            group_res.entry_s['cn'] = [group_name]
            if 'memberUid' not in group_res.entry_s:
                # fall-back to member attribute
                group_res.entry_s['memberUid'] = [
                    user_dn.split(',', 1)[0][4:]
                    for user_dn in group_res.entry_s.get('member', [])
                ]
            all_user_names.update(group_res.entry_s['memberUid'])
            group_map[gid_number] = UsersUpdater._group_convert(group_res.entry_s)
            group_name_map[group_name] = gid_number
            group_dn2id_map[group_res.dn_s] = gid_number
            self._log(logging.DEBUG, 'POSIX group: %r', group_map[gid_number])
            for role_attr in role_groups:
                if 'memberUid' in group_res.entry_s and group_res.dn_s in role_groups[role_attr]:
                    role_gid_number = CFG.vgroup_role_map[role_attr][0]
                    group_map[role_gid_number][3].update(group_res.entry_s['memberUid'])
        self._log(logging.DEBUG, 'Role group mappings: %r', role_groups)

        self._check_group_timestamps(group_results)

        self._export_sudoers(sudoers_results, role_groups)

        # sanity checks
        if len(group_map) != len(group_results)+len(CFG.vgroup_role_map):
            self._log(
                logging.WARN,
                'Different group length! group_map=%d group_results=%d',
                len(group_map),
                len(group_results),
            )

        return (
            group_map,
            group_name_map,
            group_dn2id_map,
            role_groups,
            all_user_names,
        )
        # end of UsersUpdater._get_group_maps()

    def _get_passwd_maps(self, ldap_conn, group_dn2id_map, role_groups):
        # init passwd map dictionaries
        passwd_map = {CFG.aehost_vaccount_t[2]: CFG.aehost_vaccount_t}
        passwd_name_map = {CFG.aehost_vaccount_t[0]: CFG.aehost_vaccount_t[2]}
        user_group_dn_list = group_dn2id_map.keys()
        if not user_group_dn_list:
            self._log(logging.WARN, 'No visible groups at all => skip searching users')
            return passwd_map, passwd_name_map
        full_user_refresh = (
            role_groups['aeDisplayNameGroups'] != self._last_role_groups['aeDisplayNameGroups'] or
            role_groups['aeVisibleGroups'] != self._last_role_groups['aeVisibleGroups'] or
            role_groups['aeLoginGroups'] != self._last_role_groups['aeLoginGroups']
        )
        memberof_filter = ldap0.filter.compose_filter(
            '|',
            ldap0.filter.map_filter_parts('memberOf', user_group_dn_list),
        )
        if full_user_refresh:
            # groups changed => do full search for users changed until now
            user_filter = memberof_filter
        else:
            # groups did not change => we can do delta-search for users changed after last run
            user_filter = '(&{memberof}(modifyTimestamp>={timestamp}))'.format(
                memberof=memberof_filter,
                timestamp=strf_secs(self._last_run),
            )
        user_attrs = (
            self.posix_account_attrs
            + int(bool(role_groups['aeDisplayNameGroups'])) * ['cn']
        )
        self._log(logging.DEBUG, 'User search filter: %r', user_filter)
        self._log(logging.DEBUG, 'User attributes: %r', user_attrs)
        # search user entries
        msg_id = ldap_conn.search(
            ldap_conn.search_base,
            ldap0.SCOPE_SUBTREE,
            filterstr=user_filter,
            attrlist=user_attrs,
        )
        if msg_id is None:
            self._log(
                logging.WARN,
                'Searching users with filter %r failed (msg_id = %r)',
                user_filter,
                msg_id
            )
            return passwd_map, passwd_name_map
        sshkeys_usernames = set()
        for res in ldap_conn.results(msg_id, timeout=CFG.timelimit):
            for user in res.rdata:
                self._log(logging.DEBUG, 'Found user entry %r : %r', user.dn_s, user.entry_s)
                # extract user account name from DN
                user_name = user.dn_s.split(',', 1)[0][4:]
                user.entry_s['uid'] = [user_name]
                uid_number = int(user.entry_s['uidNumber'][0])
                passwd_map[uid_number] = UsersUpdater._passwd_convert(user.entry_s)
                passwd_name_map[user_name] = uid_number
                if CFG.sshkeys_dir:
                    # store user's SSH key
                    if 'sshPublicKey' in user.entry_s:
                        self._store_ssh_key(user)
                        sshkeys_usernames.add(user_name)
                    else:
                        self._delete_ssh_key(user_name)
        # trigger removal of obsolete SSH keys
        if CFG.sshkeys_dir and full_user_refresh:
            self._delete_obsolete_keys(sshkeys_usernames)
        return passwd_map, passwd_name_map
        # end of UsersUpdater._get_passwd_maps()

    def _delete_ssh_key(self, user_name):
        sshkey_filename = os.path.join(CFG.sshkeys_dir, user_name)
        if not os.path.exists(sshkey_filename):
            self._log(logging.DEBUG, 'No SSH key file %r found', sshkey_filename)
            return
        self._log(logging.INFO, 'Removing SSH key file %r', sshkey_filename)
        try:
            os.remove(sshkey_filename)
        except OSError as os_error:
            self._log(
                logging.ERROR,
                'Error removing SSH key file %r: %r',
                sshkey_filename,
                os_error,
            )

    def _delete_obsolete_keys(self, active_userid_set):
        """
        remove SSH keys for usernames not in `active_userid_set'
        """
        existing_ssh_key_files = glob.glob(os.path.join(CFG.sshkeys_dir, '*'))
        path_prefix_len = len(CFG.sshkeys_dir) + 1
        self._log(
            logging.DEBUG,
            '%d existing SSH key files found: %r',
            len(existing_ssh_key_files),
            existing_ssh_key_files
        )
        old_userid_set = {
            p[path_prefix_len:]
            for p in existing_ssh_key_files
        }
        self._log(
            logging.DEBUG,
            '%d existing user IDs: %s',
            len(old_userid_set),
            ', '.join(map(str, old_userid_set))
        )
        to_be_removed = old_userid_set - active_userid_set
        if to_be_removed:
            self._log(
                logging.INFO,
                '%d existing files to be removed: %s',
                len(to_be_removed),
                ', '.join(map(str, to_be_removed))
            )
            for user_name in to_be_removed:
                self._delete_ssh_key(user_name)
        # end of SSHKeysUpdater._refresh_task()

    def _refresh_task(self, ldap_conn):
        """
        Search users and groups
        """

        # init map dictionaries and search map entries
        #-------------------------------------------------------------------
        group_map, group_name_map, group_dn2id_map, \
            role_groups, all_user_names = self._get_group_maps(ldap_conn)
        passwd_map, passwd_name_map = self._get_passwd_maps(
            ldap_conn, group_dn2id_map, role_groups
        )
        group_member_map = self._group_membership_map(group_map, passwd_name_map)

        # determine UID set of all user names seen in group entries
        #-------------------------------------------------------------------
        self._log(logging.DEBUG, 'all_user_names = %r', all_user_names)
        new_passwd_keys = set()
        for user_name in list(all_user_names):
            if user_name in passwd_name_map:
                new_passwd_keys.add(passwd_name_map[user_name])
            elif user_name in passwd.PASSWD_NAME_MAP:
                new_passwd_keys.add(passwd.PASSWD_NAME_MAP[user_name])
        new_passwd_keys.add(CFG.aehost_vaccount_t[2])
        self._log(logging.DEBUG, 'new_passwd_keys = %r', new_passwd_keys)

        # update global passwd map dictionaries
        #-------------------------------------------------------------------
        passwd_key_set = set(passwd.PASSWD_MAP)
        add_passwd_keys = new_passwd_keys - passwd_key_set
        remove_passwd_keys = passwd_key_set - new_passwd_keys
        passwd.PASSWD_MAP.update(passwd_map)
        passwd.PASSWD_NAME_MAP.update(passwd_name_map)
        group.GROUP_MEMBER_MAP.update(group_member_map)
        if add_passwd_keys:
            self._log(
                logging.INFO,
                '%d passwd entries added: %s',
                len(add_passwd_keys),
                ','.join([
                    passwd.PASSWD_MAP[uid_number][0]
                    for uid_number in add_passwd_keys
                ])
            )
        if remove_passwd_keys:
            remove_passwd_names = ','.join([
                passwd.PASSWD_MAP[uid_number][0]
                for uid_number in remove_passwd_keys
            ])
            for uid_number in remove_passwd_keys:
                self._log(
                    logging.DEBUG,
                    'Removing %r from passwd map',
                    passwd.PASSWD_MAP[uid_number][0],
                )
                dict_del(passwd.PASSWD_NAME_MAP, passwd.PASSWD_MAP[uid_number][0])
                dict_del(group.GROUP_MEMBER_MAP, passwd.PASSWD_MAP[uid_number][0])
                del passwd.PASSWD_MAP[uid_number]
            self._log(
                logging.INFO,
                '%d passwd entries removed: %s',
                len(remove_passwd_keys),
                remove_passwd_names,
            )
        self._log(logging.DEBUG, '%d passwd entries', len(passwd.PASSWD_MAP))
        if not (
                len(passwd.PASSWD_MAP) ==
                len(passwd.PASSWD_NAME_MAP) ==
                len(group.GROUP_MEMBER_MAP)
            ):
            self._log(
                logging.WARN,
                (
                    'Different passwd map length! '
                    'PASSWD_MAP=%d PASSWD_NAME_MAP=%d GROUP_MEMBER_MAP=%d'
                ),
                len(passwd.PASSWD_MAP),
                len(passwd.PASSWD_NAME_MAP),
                len(group.GROUP_MEMBER_MAP),
            )
            self._log(
                logging.DEBUG,
                'PASSWD_MAP = %s',
                pprint.pformat(passwd.PASSWD_MAP, indent=2),
            )
            self._log(
                logging.DEBUG,
                'PASSWD_NAME_MAP = %s',
                pprint.pformat(passwd.PASSWD_NAME_MAP, indent=2),
            )
            self._log(
                logging.DEBUG,
                'GROUP_MEMBER_MAP = %s',
                pprint.pformat(group.GROUP_MEMBER_MAP, indent=2),
            )

        # augment posixGroup entries with virtual groups
        # derived from posixAccount entries
        #-------------------------------------------------------------------
        for uid_number in new_passwd_keys:
            pw_entry = passwd.PASSWD_MAP[uid_number]
            # Safety first! Do not assume UID and GID are equal!
            gid_number = pw_entry[2]
            if gid_number in group_map:
                continue
            group_name = ''.join((
                CFG.vgroup_name_prefix,
                pw_entry[0],
            ))
            group_map[gid_number] = UsersUpdater._group_convert({
                'cn': [group_name],
                'gidNumber': [gid_number],
            })
            group_name_map[group_name] = gid_number
            self._log(
                logging.DEBUG,
                'Primary user group entry for %d : %r',
                gid_number,
                group_map[gid_number],
            )

        # update global group map dictionaries
        #-------------------------------------------------------------------
        new_group_keys = set(group_map.keys())
        group_key_set = set(group.GROUP_MAP)
        add_group_keys = new_group_keys - group_key_set
        remove_group_keys = group_key_set - new_group_keys
        group.GROUP_MAP.update(group_map)
        group.GROUP_NAME_MAP.update(group_name_map)
        if add_group_keys:
            self._log(
                logging.INFO,
                '%d group entries added: %s',
                len(add_group_keys),
                ','.join([
                    group.GROUP_MAP[group_dn][0]
                    for group_dn in add_group_keys
                ])
            )
        if remove_group_keys:
            remove_group_names = ','.join([
                group.GROUP_MAP[gid_number][0]
                for gid_number in remove_group_keys
            ])
            for gid_number in remove_group_keys:
                dict_del(group.GROUP_NAME_MAP, group.GROUP_MAP[gid_number][0])
                del group.GROUP_MAP[gid_number]
                self._log(logging.DEBUG, 'Removed %d from group map', gid_number)
            self._log(
                logging.INFO,
                '%d group entries removed: %s',
                len(remove_group_keys),
                remove_group_names,
            )
        self._log(logging.DEBUG, '%d group entries', len(group.GROUP_MAP))

        # save state
        self._last_role_groups = role_groups

        # end of _refresh_task()

    def _reset_last_groups(self):
        # reset state for delta sync
        self._last_role_groups = {
            role_attr: set()
            for role_attr in CFG.vgroup_role_map
        }

    def reset(self):
        """
        trigger next run, skips refresh sleep time
        """
        self._reset_last_groups()
        RefreshThread.reset(self)

    def get_monitor_data(self):
        """
        returns all monitoring data as dict
        """
        res = RefreshThread.get_monitor_data(self)
        res.update(dict(
            group_count=len(group.GROUP_MAP),
            group_member_count=len(group.GROUP_MEMBER_MAP),
            group_name_count=len(group.GROUP_NAME_MAP),
            passwd_count=len(passwd.PASSWD_MAP),
            passwd_name_count=len(passwd.PASSWD_NAME_MAP),
        ))
        return res


class NetworkAddrUpdater(RefreshThread):
    """
    Thread spawned to update hosts map cache
    """
    hosts_attrs = [
        'aeFqdn',
        'ipHostNumber',
        'macAddress',
    ]

    def _refresh_task(self, ldap_conn):
        """
        Refresh the hosts map
        """
        hosts_map = {}
        hosts_name_map = {}
        hosts_addr_map = {}
        netaddr_base = str(DNObj.from_str(ldap_conn.get_whoami_dn()).slice(CFG.netaddr_level, None))
        self._log(logging.DEBUG, 'Searching network address entries beneath %r', netaddr_base)
        ldap_results = ldap_conn.search_s(
            netaddr_base,
            ldap0.SCOPE_SUBTREE,
            filterstr='(objectClass=aeNwDevice)',
            attrlist=self.hosts_attrs,
        )
        for nw_res in ldap_results:
            hosts_map[nw_res.dn_s] = nw_res.entry_s
            for name in nw_res.entry_s['aeFqdn']:
                hosts_name_map[name] = nw_res.dn_s
            for addr in nw_res.entry_s['ipHostNumber']:
                hosts_addr_map[addr] = nw_res.dn_s
        # update hosts map dictionaries
        hosts_key_set = set(hosts.HOSTS_MAP.keys())
        new_hosts_keys = set(hosts_map.keys())
        add_hosts_keys = new_hosts_keys - hosts_key_set
        remove_hosts_keys = hosts_key_set - new_hosts_keys
        hosts.HOSTS_MAP.update(hosts_map)
        hosts.HOSTS_NAME_MAP.update(hosts_name_map)
        hosts.HOSTS_ADDR_MAP.update(hosts_addr_map)
        self._log(
            logging.DEBUG,
            '%d hosts entries, added %d, removed %d',
            len(hosts.HOSTS_MAP),
            len(add_hosts_keys),
            len(remove_hosts_keys),
        )
        if remove_hosts_keys:
            for nw_dn in remove_hosts_keys:
                try:
                    ldap_res = ldap_conn.read_s(nw_dn, attrlist=['1.1'])
                    if ldap_res is None:
                        raise ldap0.NO_SUCH_OBJECT()
                except (ldap0.NO_SUCH_OBJECT, ldap0.INSUFFICIENT_ACCESS):
                    for name in hosts.HOSTS_MAP[nw_dn]['aeFqdn']:
                        dict_del(hosts.HOSTS_NAME_MAP, name)
                    for addr in hosts.HOSTS_MAP[nw_dn]['ipHostNumber']:
                        dict_del(hosts.HOSTS_ADDR_MAP, addr)
                    del hosts.HOSTS_MAP[nw_dn]
                    self._log(logging.DEBUG, 'Removed %r from group map', nw_dn)
                else:
                    self._log(
                        logging.WARN,
                        '%r marked to be deleted, but found %r => abort refresh',
                        nw_dn,
                        ldap_res,
                    )
                    return
            self._log(
                logging.DEBUG,
                '%d hosts entries removed: %s',
                len(remove_hosts_keys),
                remove_hosts_keys,
            )
        # end of _refresh_task()

    def get_monitor_data(self):
        """
        returns all monitoring data as dict
        """
        res = RefreshThread.get_monitor_data(self)
        res.update(dict(
            hosts_addr_count=len(hosts.HOSTS_ADDR_MAP),
            hosts_count=len(hosts.HOSTS_MAP),
            hosts_name_count=len(hosts.HOSTS_NAME_MAP),
        ))
        return res


USERSUPDATER_TASK = None
