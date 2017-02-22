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
    :created: 02-21-2017 18:57:46
    :modified: 02-21-2017 18:57:46
.. moduleauthor:: Stephen Bunn <r>
"""

import abc
import multiprocessing

import blinker

from ..requester._common import AbstractRequester


class AbstractScheduler(multiprocessing.Process):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        super().__init__()

    @abc.abstractproperty
    def signal_name(self) -> str:
        raise NotImplementedError()

    @abc.abstractproperty
    def signal(self) -> blinker.Signal:
        raise NotImplementedError()

    @abc.abstractproperty
    def requester(self) -> AbstractRequester:
        raise NotImplementedError()

    @abc.abstractmethod
    def run(self) -> None:
        raise NotImplementedError()
