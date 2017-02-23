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

    _signal_template = (
        '{self.__class__.__name__}_{self.delay}({self._requester.signal_name})'
    )

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
    def signal_name(self) -> str:
        """ The signal name of the Obvious scheduler (extends requester's).
        """

        return self._signal_template.format(self=self)

    @property
    def signal(self) -> blinker.Signal:
        """ The signal of the Obvious scheduler.
        """

        return blinker.signal(self.signal_name)

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
        self._delay = delay

    def run(self):
        """ Starts the infinite loop for signaling scheduled requests.
        """

        while self.is_alive():
            self.signal.send(self)
            time.sleep(self.delay)
