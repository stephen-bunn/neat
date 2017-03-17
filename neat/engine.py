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

import queue
import multiprocessing
from typing import Dict, List

import blinker
import jsonschema

from . import const
from .scheduler._common import AbstractScheduler
from .requester._common import AbstractRequester
from .translator._common import AbstractTranslator
from .translator import get_translator
from .models.record import Record


class Engine(object):

    def __init__(
        self,
        register: Dict[AbstractScheduler, AbstractRequester]={},
        cpu_count: int=None
    ):
        self.record_queue = queue.Queue()
        self.register = register
        self._cpu_count = (
            multiprocessing.cpu_count()
            if not cpu_count or not isinstance(cpu_count, int) else
            cpu_count
        )
        self._translators = {}

    @property
    def register(self) -> Dict[AbstractScheduler, AbstractRequester]:
        return self._register

    @register.setter
    def register(
        self,
        register: Dict[AbstractScheduler, AbstractRequester]
    ) -> None:
        self._register = register

    @property
    def translators(self) -> List[AbstractTranslator]:
        return self._translators

    def on_scheduled(self, scheduler: AbstractScheduler) -> None:
        const.log.debug((
            'scheduled request from scheduler `{scheduler}` ...'
        ).format(scheduler=scheduler))
        self.register[scheduler].request()

    def on_data(
        self,
        requester: AbstractRequester, data: str, meta: dict
    ) -> None:
        const.log.debug((
            'recieved data from requester `{requester}` ...'
        ).format(requester=requester, data=data))
        if requester.__class__.__name__ not in self.translators:
            translator = get_translator(requester.__class__.__name__)()
            translator.signal.connect(self.on_record)
            self.translators[requester.__class__.__name__] = \
                get_translator(requester.__class__.__name__)()
        self.translators[requester.__class__.__name__]\
            .translate(data, meta=meta)

    def on_record(self, record: Record) -> None:
        if not record.validate():
            const.log.error((
                'invalid record recieved `{record}` ...'
            ).format(record=record))
        else:
            const.log.debug((
                'adding record `{record}` to record queue ...'
            ).format(record=record))
            self.record_queue.put(record)

    def start(self) -> None:
        const.log.info((
            'starting engine with `{self._cpu_count}` cpus for '
            '`{self.register}` ...'
        ).format(self=self))

        for (scheduler, requester) in self.register.items():
            scheduler.signal.connect(self.on_scheduled)
            requester.signal.connect(self.on_data)
            scheduler.start()

            const.log.info((
                'starting scheduler `{scheduler}` signal as daemon '
                'with pid `{scheduler.pid}` for `{requester}` ...'
            ).format(scheduler=scheduler, requester=requester))

    def stop(self) -> None:
        const.log.info((
            'stopping engine and scheduler threads with pids '
            '{scheduler_pids} ...'
        ).format(scheduler_pids=[_.pid for _ in self.register.keys()]))

        for (scheduler, requester) in self.register.items():
            const.log.debug((
                'ensuring scheduler `{scheduler}` with pid '
                '`{scheduler.pid}` is terminated ...'
            ).format(scheduler=scheduler))
            scheduler.terminate()
