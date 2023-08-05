# -*- coding: ascii -*-
"""
aehostd.config - routines for getting configuration information
"""

from .cfg import CFG
from . import req


CONFIG_REQ_GET = 0x00010001

CONFIG_PASSWORD_PROHIBIT_MESSAGE = 1


class ConfigGetRequest(req.Request):
    """
    handle password change requests (mainly denying them)
    """
    rtype = CONFIG_REQ_GET
    msg_format = (
        ('cfgopt', int),
    )

    def process(self):
        """
        reject the password change request
        """
        if self._params.get('cfgopt', None) == CONFIG_PASSWORD_PROHIBIT_MESSAGE:
            self._msgio.write_int32(req.RES_BEGIN)
            self._msgio.write_str(CFG.pam_passmod_deny_msg or '')
        self._msgio.write_int32(req.RES_END)
