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
    :created: 02-16-2017 15:57:47
    :modified: 02-16-2017 15:57:47
.. moduleauthor:: Stephen Bunn <r>
"""

import abc

import blinker


class AbstractRequester(object):
    """ The abstract class for requester classes.
    """
    __metaclass__ = abc.ABCMeta

    @property
    def signal(self) -> blinker.Signal:
        """ The unique signal for the requester when complete.
        """

        if not hasattr(self, '_signal') or not self._signal:
            self._signal = blinker.Signal()
        return self._signal

    @abc.abstractmethod
    def request(self) -> None:
        """ The requester method for making requests.
        """

        raise NotImplementedError()

    @abc.abstractmethod
    def receive(self) -> None:
        """ The receiver method for getting data from requests.
        """

        raise NotImplementedError()
