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
import jsonschema

from . import const
from .scheduler._common import AbstractScheduler
from .requester._common import AbstractRequester
from .translator._common import AbstractTranslator
from .translator import get_translator


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
        self._translators = {}

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

    @property
    def translators(self) -> List[AbstractTranslator]:
        return self._translators

    def on_scheduled(self, scheduler: AbstractScheduler) -> None:
        const.log.debug((
            'scheduled request from scheduler `{scheduler}` ...'
        ).format(scheduler=scheduler))
        scheduler.requester.request()

    def on_data(self, requester: AbstractRequester, data: str) -> None:
        if requester.__class__.__name__ not in self.translators:
            self._translators[requester.__class__.__name__] = \
                get_translator(requester)()
        translator = self.translators[requester.__class__.__name__]
        if translator.validate(data):
            record = translator.translate(data)
            try:
                jsonschema.validate(record, const.record_schema)
                # TODO: do something
            except jsonschema.exceptions.ValidationError as exc:
                const.log.error((
                    'invalid record format built by `{translator}` ...'
                ).format(translator=translator))
                const.log.exception(exc)

    def start(self) -> None:
        const.log.info((
            'starting engine with `{self._cpu_count}` cpus for '
            '`{scheulers}` scheulers ...'
        ).format(self=self, scheulers=len(self.schedulers)))

        for scheduler in self.schedulers:
            scheduler.signal.connect(self.on_scheduled)
            scheduler.requester.signal.connect(self.on_data)
            scheduler.daemon = True
            scheduler.start()

            const.log.info((
                'starting scheduler `{scheduler}` signal as daemon '
                'with pid `{scheduler.pid}` ...'
            ).format(scheduler=scheduler))

        for _ in self.schedulers:
            _.join()
