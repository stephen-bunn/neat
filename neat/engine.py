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

import sys
import queue
import itertools
import threading
import multiprocessing
from typing import Dict, List

import blinker
import jsonschema

from . import const
from .models.record import Record
from .scheduler._common import AbstractScheduler
from .requester._common import AbstractRequester
from .translator._common import AbstractTranslator
from .pipe._common import AbstractPipe
from .translator import get_translator


class Engine(object):

    def __init__(
        self,
        register: Dict[AbstractScheduler, AbstractRequester]={},
        pipes: List[AbstractPipe]=[],
        cpu_count: int=None, queue_size: int=None
    ):
        self.record_queue = queue.Queue(maxsize=(
            (len(register.keys()) * 3)
            if not queue_size or not isinstance(queue_size, int) else
            queue_size
        ))
        self._register = register
        self._pipes = pipes
        self._cpu_count = (
            multiprocessing.cpu_count()
            if not cpu_count or not isinstance(cpu_count, int) else
            cpu_count
        )
        self._translators = {}
        self._pipe_threads = {}

    @property
    def register(self) -> Dict[AbstractScheduler, AbstractRequester]:
        return self._register

    @property
    def translators(self) -> List[AbstractTranslator]:
        return self._translators

    @property
    def pipes(self) -> List[AbstractPipe]:
        return self._pipes

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
            if self.record_queue.full():
                queued = []
                while not self.record_queue.empty():
                    queued.append(self.record_queue.get())
                self.on_full(queued)

    def on_full(self, records: List[Record]) -> None:
        for committer in self.pipes:
            committer_thread = threading.Thread(
                target=committer.commit, args=(records,),
                name=(
                    '{committer.__class__.__name__}-Thread'
                ).format(committer=committer),
            )
            if committer not in self._pipe_threads:
                self._pipe_threads[committer] = []
            self._pipe_threads[committer].append(committer_thread)
            committer_thread.start()
            const.log.debug((
                'starting commit process for `{committer}` on thread '
                '`{committer_thread.name}` ...'
            ).format(committer=committer, committer_thread=committer_thread))

    def on_complete(self, committer: AbstractPipe) -> None:
        const.log.debug((
            'pipe `{committer}` completed, removing dead threads ...'
        ).format(committer=committer))
        for thread in self._pipe_threads[committer]:
            if not thread.is_alive():
                self._pipe_threads[committer].remove(thread)

    def start(self) -> None:
        const.log.info((
            'starting engine with `{self._cpu_count}` cpus for '
            '`{self.register}` ...'
        ).format(self=self))

        if len(self.pipes) <= 0:
            const.log.warning((
                'no pipes have been added to the engine, '
                'records will not be saved ...'
            ))
            self.record_queue = queue.Queue(maxsize=0)
        else:
            for committer in self.pipes:
                if not committer.validate():
                    const.log.warning((
                        'pipe `{committer}` did not pass validation, '
                        'removing from pipes ...'
                    ).format(committer=committer))
                    self.pipes.remove(committer)

        for committer in self.pipes:
            committer.signal.connect(self.on_complete)

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

        still_alive = list(itertools.chain(
            *self._pipe_threads.values()
        ))
        if len(still_alive) > 0:
            const.log.debug((
                'transactions {still_alive} are still in progress, '
                'KeyboardInterrupt again for forced stop ...'
            ).format(still_alive=still_alive))
            try:
                for thread in still_alive:
                    thread.join()
            except KeyboardInterrupt:
                const.log.warning(('forcing stop ...'))
                sys.exit(0)
