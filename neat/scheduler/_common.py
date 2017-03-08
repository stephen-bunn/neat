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
    """ The abstract scheduler which all schedulers much extend.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        """ The abstract scheduler initializer.

        ..note: Required that all subclasses super initialization
        """

        super().__init__()

    @property
    def signal(self) -> blinker.Signal:
        """ The unique signal of the scheduler.
        """

        if not hasattr(self, '_signal') or not self._signal:
            self._signal = blinker.Signal()
        return self._signal

    @abc.abstractproperty
    def requester(self) -> AbstractRequester:
        """ The requester object to schedule.
        """

        raise NotImplementedError()

    @abc.abstractmethod
    def run(self) -> None:
        """ The infinite method to start sending signals on scheduled delays.
        """

        raise NotImplementedError()
