#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# GNU GPLv3 <https://www.gnu.org/licenses/gpl-3.0.en.html>

import abc
import multiprocessing

import blinker


class AbstractScheduler(multiprocessing.Process, metaclass=abc.ABCMeta):
    """ The abstract scheduler which all schedulers much extend.
    """
    signal = blinker.Signal()

    def __init__(self):
        """ The abstract scheduler initializer.

        ..note: Required that all subclasses super initialization
        """

        super().__init__()

    @abc.abstractmethod
    def run(self) -> None:
        """ The infinite method to start sending signals on scheduled delays.
        """

        raise NotImplementedError()
