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

from ._common import AbstractScheduler
from ..requester import ObviousRequester


class ObviousScheduler(AbstractScheduler):

    _signal_template = (
        '{self.__class__.__name__}_{self.delay}({self._requester.signal_name})'
    )

    def __init__(self, requester: ObviousRequester, delay: int=1):
        super().__init__()
        self._requester = requester
        self.delay = delay

    @property
    def signal_name(self) -> str:
        return self._signal_template.format(self=self)

    @property
    def signal(self) -> blinker.Signal:
        return blinker.signal(self.signal_name)

    @property
    def requester(self) -> ObviousRequester:
        return self._requester

    @property
    def delay(self) -> int:
        return self._delay

    @delay.setter
    def delay(self, delay: int) -> None:
        self._delay = delay

    def run(self):
        while self.is_alive():
            self.signal.send(self)
            time.sleep(self.delay)
