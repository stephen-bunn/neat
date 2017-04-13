#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# GNU GPLv3 <https://www.gnu.org/licenses/gpl-3.0.en.html>

import abc
from typing import List

from ..models import Record

import blinker


class AbstractPipe(object, metaclass=abc.ABCMeta):
    """ The base class for all valid pipes.
    """

    signal = blinker.Signal()

    @abc.abstractmethod
    def accept(self, record: Record) -> None:
        """ Accepts a record for placement in the pipe

        .. note:: Does not ensure placement in the pipe if engine is closing

        :param record: The record to place in the pipe
        :type record: Record
        :returns: Does not return
        :rtype: None
        """

        raise NotImplementedError()

    @abc.abstractmethod
    def validate(self) -> bool:
        """ Self validates the pipe.

        :returns: True if the pipe is value, otherwise False
        :rtype: bool
        """

        raise NotImplementedError()
