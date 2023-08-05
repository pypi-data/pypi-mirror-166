# -*- coding: ascii -*-
"""
aehostd.req - base stuff for processing requests
"""

import logging
import inspect
import struct
import socket
from importlib import import_module
from io import BytesIO
from typing import Sequence
from socket import inet_pton


# The following constants have to match content of nslcd.h
PROTO_VERSION = 0x00000002
RES_BEGIN = 1
RES_END = 2


class DummySocket(BytesIO):
    """
    Socket emulation class with .recv() method
    """

    def recv(self, numbytes: int) -> bytes:
        return self.read(numbytes)


class MsgIO:
    """
    I/O object for low-level processing of request input and response output
    """
    __slots__ = (
        '_out',
        '_int32',
        '_sock',
        'rtype',
    )

    def __init__(self, sock):
        # int32 decoder/encoder
        self._int32 = struct.Struct('!i')
        # initialize input stream
        self._sock = sock
        nslcd_version = self.read_int32()
        if nslcd_version != PROTO_VERSION:
            raise ValueError(
                'Wrong protocol version: Expected %d but got %d' % (
                    PROTO_VERSION,
                    nslcd_version,
                )
            )
        self.rtype = self.read_int32()
        # initialize the output stream
        self._out = BytesIO()
        self.write_int32(PROTO_VERSION)

    @property
    def response(self) -> bytes:
        """
        returns the generated response
        """
        return self._out.getvalue()

    def read(self, numbytes) -> bytes:
        res = []
        recv_bytes = 0
        while recv_bytes < numbytes:
            buf = self._sock.recv(numbytes-recv_bytes)
            recv_bytes += len(buf)
            res.append(buf)
        return b''.join(res)

    def read_int32(self) -> int:
        """
        read an 32-bit integer from the request
        """
        return self._int32.unpack(self.read(self._int32.size))[0]

    def read_str(self) -> str:
        """
        read a string from the request
        """
        val_l = self.read_int32()
        val_b = self.read(val_l)
        return val_b.decode('utf-8')

    def read_ipaddr(self) -> str:
        """
        Read an address (IPv4 or IPv6) from the stream
        and return it as string representation.
        """
        addr_family = self.read_int32()
        val_l = self.read_int32()
        if val_l > 64:
            raise ValueError('Expected max. length of 64, got %d' % (val_l,))
        val_b = self.read(val_l)
        return socket.inet_ntop(addr_family, val_b)

    def write_int32(self, value: int) -> None:
        """
        Write a 32-bit int to response data
        """
        self._out.write(self._int32.pack(value))

    def write_str(self, value: str) -> None:
        """
        Write a string to response data
        """
        val_b = value.encode('utf-8')
        self.write_int32(len(val_b))
        self._out.write(val_b)

    def write_list(self, value: Sequence[str]) -> None:
        """
        Write a list of strings to response data
        """
        self.write_int32(len(value))
        for string in value:
            self.write_str(string)

    def write_ipaddr(self, value: str) -> None:
        """
        Write an address (usually IPv4 or IPv6).
        """
        try:
            addr_family, address = socket.AF_INET, inet_pton(socket.AF_INET, value)
        except socket.error:
            addr_family, address = socket.AF_INET6, inet_pton(socket.AF_INET6, value)
        self.write_int32(addr_family)
        self.write_int32(len(address))
        self._out.write(address)


class Request:
    """
    Request handler class. Subclasses are expected to handle actual requests
    and should implement the following members:

      rtype - the request type handled by a class

      read_params() - a function that reads the request params of the
                          request stream
      write() - function that writes a single LDAP entry to the result stream

    """
    __slots__ = (
        '_msgio',
        'msgio',
        'server',
        'peer',
        '_log_prefix',
        '_params',
    )
    rtype = None
    msg_format = (())

    def __init__(self, msgio, peer):
        self.msgio = self._msgio = msgio
        self.peer = peer
        self._log_prefix = self._get_log_prefix()
        self._params = None

    def _get_log_prefix(self):
        pid, uid, gid = self.peer
        return 'pid=%d uid=%d gid=%d %s' % (pid, uid, gid, self.__class__.__name__)

    def _log(self, log_level, msg, *args, **kwargs):
        msg = ' '.join((self._log_prefix, msg))
        logging.log(log_level, msg, *args, **kwargs)

    def read_params(self) -> dict:
        """
        Read and return the input params from the input stream
        """
        self._params = {}
        for pname, ptype in self.msg_format:
            if ptype == str:
                self._params[pname] = self._msgio.read_str()
            elif ptype == int:
                self._params[pname] = self._msgio.read_int32()
            elif ptype == 'ip':
                self._params[pname] = self._msgio.read_ipaddr()
            else:
                raise TypeError('Unknown parameter type {0!r} for parameter {1}'.format(
                    ptype, pname,
                ))

    @classmethod
    def synthesize(cls, params) -> bytes:
        """
        Synthesize a request from parameters and return the raw byte sequence
        """
        i32 = struct.Struct('!i')
        msgio = MsgIO(
            DummySocket(b''.join((
                i32.pack(PROTO_VERSION),
                i32.pack(cls.rtype),
            )))
        )
        msgio.write_int32(cls.rtype)
        for pname, ptype in cls.msg_format:
            if ptype == str:
                msgio.write_str(params.get(pname, ''))
            elif ptype == int:
                msgio.write_int32(params.get(pname, 0))
            elif ptype == 'ip':
                msgio.write_ipaddr(params.get(pname, b''))
            else:
                raise TypeError('Unknown parameter type {0!r} for parameter {1}'.format(
                    ptype, pname,
                ))
        return msgio.response

    def get_results(self, params):
        """
        get results for params
        """
        return []

    def write(self, result):
        """
        send result to client
        just a place holder must be over-written by derived classes
        """
        raise RuntimeError(
            '%s.write() must not be directly used!' % (self.__class__.__name__,)
        )

    def process(self):
        """
        This method handles the request based on the params read
        with read_params().
        """
        res_count = 0
        for res in self.get_results(self._params):
            res_count += 1
            self._log(logging.DEBUG, 'res#%d: %r', res_count, res)
            self._msgio.write_int32(RES_BEGIN)
            self.write(res)
        if not res_count:
            self._log(logging.DEBUG, 'no result')
        # write the final result code
        self._msgio.write_int32(RES_END)

    def fail(self):
        """
        called in case request parameters could not be parsed
        """
        self._msgio.write_int32(self.rtype)
        self._msgio.write_int32(RES_BEGIN)
        self._msgio.write_int32(RES_END)

    def log_params(self, log_level):
        """
        log request parameters
        """
        self._log(log_level, '(%r)', self._params)


def get_handlers(module_name):
    """
    Return a dictionary mapping request types to Request handler classes.
    """
    res = {}
    module = import_module(module_name)
    logging.debug('Inspecting module %s: %s', module_name, module)
    for _, cls in inspect.getmembers(module, inspect.isclass):
        if (
                issubclass(cls, Request)
                and hasattr(cls, 'rtype')
                and cls.rtype is not None
            ):
            res[cls.rtype] = cls
    logging.debug(
        'Registered %d request classes in module %s: %s',
        len(res),
        module_name,
        ', '.join([cls.__name__ for cls in res.values()]),
    )
    return res
