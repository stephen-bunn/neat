#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn <r>
# GNU GPLv3 <https://www.gnu.org/licenses/gpl-3.0.en.html>

"""
engine.py
.. module:: neat
    :platform: Linux, MacOSX, Win32
    :synopsis:
    :created: 02-21-2017 18:58:46
    :modified: 02-21-2017 18:58:46
.. moduleauthor:: Stephen Bunn <r>
"""

import multiprocessing
from typing import List

import blinker

from . import const
from .scheduler._common import AbstractScheduler


class Engine(object):

    def __init__(
        self,
        schedulers: List[AbstractScheduler], cpu_count: int=None
    ):
        self._cpu_count = (
            multiprocessing.cpu_count()
            if not cpu_count or not isinstance(cpu_count, int) else
            cpu_count
        )
        self.schedulers = schedulers

    @property
    def schedulers(self) -> List[AbstractScheduler]:
        return self._schedulers

    @schedulers.setter
    def schedulers(self, schedulers: List[AbstractScheduler]) -> None:
        if not all(isinstance(_, AbstractScheduler) for _ in schedulers):
            raise ValueError((
                "schedulers must be a list of subclasses of AbstractScheduler"
            ))
        self._schedulers = schedulers

    def on_scheduled(self, scheduler: AbstractScheduler) -> None:
        print(scheduler)
        # scheduler.requester.request()

    def on_data(self, data: str) -> None:
        # TODO: pass the information into the translator
        # then to the transaction
        print(data)

    def start(self) -> None:
        for scheduler in self.schedulers:
            scheduler.signal.connect(self.on_scheduled)
            scheduler.requester.signal.connect(self.on_data)
            scheduler.daemon = True
            scheduler.start()

            const.log.debug((
                'starting scheduler `{scheduler.name}` signal '
                '`{scheduler.signal_name}` as daemon with pid '
                '`{scheduler.pid}` ...'
            ).format(scheduler=scheduler))

        for _ in self.schedulers:
            _.join()
