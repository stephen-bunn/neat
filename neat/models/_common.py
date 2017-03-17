#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn <r>
# GNU GPLv3 <https://www.gnu.org/licenses/gpl-3.0.en.html>

"""
_common.py
    :platform: Linux, MacOSX, Win32
    :synopsis:
    :created: 03-13-2017 16:26:19
    :modified: 03-13-2017 16:26:19
.. moduleauthor:: Stephen Bunn <r>
"""

import abc


class AbstractModel(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def validate(self) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    def to_dict(self) -> dict:
        raise NotImplementedError()
