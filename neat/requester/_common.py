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


class AbstractRequester(object, metaclass=abc.ABCMeta):
    """ The abstract class for requester classes.
    """
    signal = blinker.Signal()

    @abc.abstractmethod
    def request(self) -> None:
        """ The requester method for making requests.
        """

        raise NotImplementedError()
