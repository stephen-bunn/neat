#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn <r>
# GNU GPLv3 <https://www.gnu.org/licenses/gpl-3.0.en.html>

"""
_common.py
    :platform: Linux, MacOSX, Win32
    :synopsis:
    :created: 02-28-2017 15:20:26
    :modified: 02-28-2017 15:20:26
.. moduleauthor:: Stephen Bunn <r>
"""

import abc


class AbstractTransaction(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def commit(self) -> None:
        raise NotImplementedError()
