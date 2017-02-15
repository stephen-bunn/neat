#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn <r>
# GNU GPLv3 <https://www.gnu.org/licenses/gpl-3.0.en.html>

"""
const.py
.. module:: neat
    :platform: Linux, MacOSX, Win32
    :synopsis:
    :created: 02-15-2017 00:46:50
    :modified: 02-15-2017 00:46:50
.. moduleauthor:: Stephen Bunn <r>
"""

import os
import sys
import logging
import logging.handlers
import datetime


class _const(object):
    _module_name = 'neat'
    _version = (0, 0, 0,)
    _authors = (
        'Stephen Bunn <stephen@bunn.io>',
        'Sierra Milosh <miloshsr1@appstate.edu>',
        'Nathan Davis <davisna1@appstate.edu>',
        'James Ward <wardja2@appstate.edu>',
    )

    __allowed_setters = (
        'log_dir', 'log_exceptions', 'log_level', 'log_format',
    )

    class ModuleConstantException(Exception):
        _code = 7001

        def __init__(self, message, code=None):
            super().__init__(message)
            self.code = (code if code else self._code)

    def __init__(self):
        self._log_exceptions = False
        self._log_level = logging.DEBUG
        self._log_format = (
            '%(asctime)s - %(levelname)s - '
            '%(filename)s:%(lineno)s;%(funcName)s '
            '%(message)s'
        )
        self._log_handlers = []

    def __setattr__(self, name, value):
        if name in self.__allowed_setters:
            super().__setattr__(name, value)
        else:
            if name in self.__dict__:
                raise self.ModuleConstantException((
                    "cannot rebind const({})"
                ).format(name))
            self.__dict__[name] = value

    def __delattr__(self, name):
        if name in self.__dict__:
            raise self.ModuleConstantException((
                "cannot unbind const({})"
            ).format(name))
        raise NameError(name)

    @property
    def module_name(self) -> str:
        return self._module_name

    @property
    def version(self) -> tuple:
        return self._version

    @property
    def base_dir(self) -> str:
        return os.path.dirname(os.path.realpath(os.path.abspath(__file__)))

    @property
    def parent_dir(self) -> str:
        return os.path.dirname(self.base_dir)

    @property
    def log_dir(self) -> str:
        if not hasattr(self, '_log_dir'):
            today = datetime.datetime.now()
            self._log_dir = os.path.join(self.parent_dir, os.sep.join([
                'logs',
                str(today.year),
                str(today.month)
            ]))
            if not os.path.isdir(self._log_dir):
                os.makedirs(self._log_dir)
        return self._log_dir

    @log_dir.setter
    def log_dir(self, value: str):
        if os.path.isdir(value):
            self._log_dir = value

    @property
    def log_level(self) -> int:
        return self._log_level

    @log_level.setter
    def log_level(self, value: int):
        self._log_level = value
        for handler in self._log_handlers:
            handler.setLevel(value)

    @property
    def log_format(self) -> str:
        return self._log_format

    @log_format.setter
    def log_format(self, value: str):
        self._log_format = value
        formatter = logging.Formatter(value)
        for handler in self._log_handlers:
            handler.setFormatter(formatter)

    @property
    def log(self) -> logging.Logger:
        if not hasattr(self, '_log'):
            self._log = logging.getLogger(self._module_name)
            self._log.setLevel(self.log_level)
            self._log.propagate = False

            today = datetime.datetime.now()
            file_handler = logging.handlers.RotatingFileHandler(
                filename=os.path.join(
                    self.log_dir,
                    '{}.log'.format(today.strftime('%m%d%Y'))
                ),
                mode='a',
                maxBytes=(1024 * 1024),
                backupCount=5
            )
            self._log_handlers.append(file_handler)
            self._log.addHandler(file_handler)

            stream_handler = logging.StreamHandler()
            self._log_handlers.append(stream_handler)
            self._log.addHandler(stream_handler)

            formatter = logging.Formatter(self.log_format)
            for handler in self._log_handlers:
                handler.setFormatter(formatter)

        return self._log

    @property
    def log_exceptions(self) -> bool:
        return self._log_exceptions

    @log_exceptions.setter
    def log_exceptions(self, value: bool):
        self._log_exceptions = value
        sys.excepthook = (
            self._exceptions_handler
            if self._log_exceptions else
            sys.excepthook
        )

    def _exception_handler(self, exctype, value, tb):
        self.log.exception((
            'EXCEPTION::{exctype} {value}'
        ).format(exctype=value.__class__.__name__, value=value))
        sys.__excepthook__(exctype, value, tb)


sys.modules[__name__] = _const()
