#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn <r>
# GNU GPLv3 <https://www.gnu.org/licenses/gpl-3.0.en.html>

"""
obvious.py
.. module:: neat
    :platform: Linux, MacOSX, Win32
    :synopsis:
    :created: 02-21-2017 19:14:57
    :modified: 02-21-2017 19:14:57
.. moduleauthor:: Stephen Bunn <r>
"""

import time
import multiprocessing

import blinker

from .. import const
from ..requester import ObviousRequester
from ._common import AbstractScheduler


class ObviousScheduler(AbstractScheduler):
    """ The scheduler for Obvious requesters.
    """

    def __init__(self, requester: ObviousRequester, delay: float=1.0):
        """ The Obvious scheduler initializer.

        :param requester: The requester to schedule
        :type requester: ObviousRequester
        :param delay: The delay to wait in between requests
        :type delay: float
        """

        super().__init__()
        self._requester = requester
        self.delay = delay

    @property
    def requester(self) -> ObviousRequester:
        """ The requester object to call for scheduled requests.
        """

        return self._requester

    @property
    def delay(self) -> float:
        """ The delay period in between scheduled requests.
        """

        return self._delay

    @delay.setter
    def delay(self, delay: float) -> None:
        """ Allows the user to modify the scheduler delay.

        :param delay: The new delay of the scheduler
        :type delay: float
        """
        self._delay = float(delay)

    def run(self):
        """ Starts the infinite loop for signaling scheduled requests.
        """

        while self.is_alive():
            self.signal.send(self)
            time.sleep(self.delay)
