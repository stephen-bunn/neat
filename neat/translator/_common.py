#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn <r>
# GNU GPLv3 <https://www.gnu.org/licenses/gpl-3.0.en.html>

"""
_common.py
.. module:: neat
    :platform: Linux, MacOSX, Win32
    :synopsis:
    :created: 02-16-2017 15:17:09
    :modified: 02-16-2017 15:17:09
.. moduleauthor:: Stephen Bunn <r>
"""

import abc


class AbstractTranslator(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def validate(self, content: str) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    def translate(self, content: str) -> dict:
        raise NotImplementedError()
