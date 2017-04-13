#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# GNU GPLv3 <https://www.gnu.org/licenses/gpl-3.0.en.html>

import abc
import multiprocessing

import blinker


class AbstractScheduler(multiprocessing.Process, metaclass=abc.ABCMeta):
    """ The base scheduler for all valid schedulers.

    .. note:: Required, that all subclasses call super initialization
    """

    signal = blinker.Signal()

    def __init__(self):
        """ The abstract scheduler initializer.
        """

        super().__init__()

    @abc.abstractmethod
    def run(self) -> None:
        """ The infinite method to start sending signals on scheduled delays.

        :returns: Does not return
        :rtype: None
        """

        raise NotImplementedError()
