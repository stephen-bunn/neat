#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# GNU GPLv3 <https://www.gnu.org/licenses/gpl-3.0.en.html>

from typing import Dict, List

from . import const
from .models.record import Record
from .scheduler._common import AbstractScheduler
from .requester._common import AbstractRequester
from .translator._common import AbstractTranslator
from .pipe._common import AbstractPipe
from .translator import get_translator

import blinker


class Engine(object):
    """ Provides communication between all of the subpackages.
    """

    on_start = blinker.Signal()
    on_stop = blinker.Signal()

    def __init__(
        self,
        register: Dict[AbstractScheduler, AbstractRequester]={},
        pipes: List[AbstractPipe]=[],
    ):
        """ Initializes an instance of the engine.

        :param register: A dictionary of schedulers mapped to requesters
        :type register: dict
        :param pipes: A list of pipes that should be used for records
        :type pipes: list
        """

        self._register = register
        self._pipes = pipes
        self._translators = {}

    @property
    def register(self) -> Dict[AbstractScheduler, AbstractRequester]:
        """ The mapping of schedulers to requesters.
        """

        return self._register

    @property
    def translators(self) -> List[AbstractTranslator]:
        """ The list of translator objects that have been needed.
        """

        return self._translators

    @property
    def pipes(self) -> List[AbstractPipe]:
        """ The list of pipe objects that are handling created records.
        """

        return self._pipes

    def on_scheduled(self, scheduler: AbstractScheduler) -> None:
        """ Event handler for when schedulers trigger their mapped requesters.

        :param scheduler: The scheduler that needs to run its requester
        :type scheduler: AbstractScheduler
        :returns: Does not return
        :rtype: None
        """

        const.log.debug((
            'scheduled request from scheduler `{scheduler}` ...'
        ).format(scheduler=scheduler))
        self.register[scheduler].request()

    def on_data(
        self,
        requester: AbstractRequester, data: str, meta: dict
    ) -> None:
        """ Event handler for when requesters get a response from their device.

        :param requester: The requester who retrieved the data
        :type requester: AbstractRequester
        :param data: The data returned from the device
        :type data: str
        :param meta: Any additional fields required to properly interpret data
        :type meta: dict
        :returns: Does not return
        :rtype: None
        """

        const.log.debug((
            'recieved data from requester `{requester}` ...'
        ).format(requester=requester, data=data))
        requester_name = requester.__class__.__name__
        if requester_name not in self.translators:
            translator = get_translator(requester_name)()
            translator.signal.connect(self.on_record)
            self.translators[requester_name] = get_translator(requester_name)()
        self.translators[requester_name].translate(data, meta=meta)

    def on_record(self, record: Record) -> None:
        """ Event handler for when translators finish translation of some data.

        :param record: The translated record
        :type record: Record
        :returns: Does not return
        :rtype: None
        """

        if not record.validate():
            const.log.error((
                'invalid record recieved `{record}` ...'
            ).format(record=record))
        else:
            const.log.debug((
                'adding record `{record}` to pipes ...'
            ).format(record=record))
            for piper in self.pipes:
                piper.accept(record)

    def on_commit(self, piper: AbstractPipe, record: Record) -> None:
        """ Event handler for when pipes finish writing out a record.

        :param piper: The pipe who wrote the record out
        :type piper: AbstractPipe
        :param record: The record that was written
        :type record: Record
        :returns: Does not return
        :rtype: None
        """
        const.log.debug((
            'pipe `{piper}` successfully handled record `{record}` ...'
        ).format(piper=piper, record=record))

    def start(self) -> None:
        """ Starts the engine.

        :returns: Does not return
        :rtype: None
        """

        self.on_start.send(self)

        for piper in self.pipes:
            if not piper.validate():
                const.log.warning((
                    'pipe `{piper}` did not pass validation, '
                    'removing from pipes ...'
                ).format(piper=piper))
                self.pipes.remove(piper)
            else:
                const.log.debug((
                    'utilizing pipe `{piper}` ...'
                ).format(piper=piper))
                piper.signal.connect(self.on_commit)

        for (scheduler, requester) in self.register.items():
            scheduler.signal.connect(self.on_scheduled)
            requester.signal.connect(self.on_data)
            scheduler.start()
            const.log.info((
                'starting scheduler `{scheduler}` signal as daemon '
                'with pid `{scheduler.pid}` for `{requester}` ...'
            ).format(scheduler=scheduler, requester=requester))

    def stop(self) -> None:
        """ Stops the engine.

        :returns: Does not return
        :rtype: None
        """

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
        self.on_stop.send(self)
