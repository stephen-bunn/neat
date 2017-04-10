#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn <r>
# GNU GPLv3 <https://www.gnu.org/licenses/gpl-3.0.en.html>

"""
rethinkdb.py
.. module::
    :platform: Linux, MacOSX, Win32
    :synopsis:
    :created: 03-17-2017 21:56:00
    :modified: 03-17-2017 21:56:00
.. moduleauthor:: Stephen Bunn <r>
"""

import time
import threading
from typing import List

from .. import const
from ..models import Record
from ._common import AbstractPipe

import rethinkdb


class RethinkDBPipe(AbstractPipe):

    def __init__(
        self, ip: str, port: int, table: str,
        clean_delay: int=300
    ):
        (self._ip, self._port) = (ip, port)
        self._table_name = table
        (self._last_cleaned, self._clean_delay) = (0, clean_delay)

        if self._table_name not in rethinkdb.table_list()\
                .run(self.connection):
            rethinkdb.table_create(self._table_name).run(self.connection)
        self.table = rethinkdb.table(self._table_name)

        self._cleaning_thread = threading.Thread(
            target=self._cleaning_scheduler,
            args=(self._clean_delay,)
        )
        self._cleaning_thread.daemon = True
        const.log.info((
            'starting `{self}` cleaning thread as daemon '
            'on `{self._clean_delay}` second delay ...'
        ).format(self=self))
        self._cleaning_thread.start()

    def __repr__(self):
        return ((
            '<{self.__class__.__name__} ({self._ip}:{self._port})>'
        ).format(self=self))

    @property
    def connection(self):
        # NOTE: unfortunately rethinkdb driver connections are not thread safe
        # For this reason, a new connection must be initalized on each request
        try:
            connection = rethinkdb.connect(
                self._ip, self._port,
                db=const.module_name
            )
            if const.module_name not in rethinkdb.db_list()\
                    .run(connection):
                rethinkdb.db_create(const.module_name)\
                    .run(connection)
            return connection
        except rethinkdb.errors.ReqlDriverError as exc:
            const.log.error((
                'could not connect to rethinkdb server at '
                '`{self._ip}:{self._port}`, {exc.message} ...'
            ).format(self=self, exc=exc))
            raise exc

    def _cleaning_scheduler(self, delay: float) -> None:
        while True:
            self.clean()
            time.sleep(delay)

    def accept(self, record: Record) -> None:
        const.log.debug((
            'commiting `{record}` records into `{self}` ...'
        ).format(self=self, record=record))
        self.table.insert(record.to_dict()).run(self.connection)
        self.signal.send(self, record=record)

    def clean(self) -> None:
        const.log.debug((
            'cleaning expired records from `{self.table}` ...'
        ).format(self=self))
        deletion_results = self.table.filter(lambda record: (
            record['timestamp'] + record['ttl']
        ) <= time.time()).delete().run(self.connection)
        const.log.debug((
            'cleaned `{deleted_count}` records from `{self.table}` ...'
        ).format(self=self, deleted_count=deletion_results['deleted']))
        self._last_cleaned = time.time()
        return deletion_results['deleted']

    def validate(self) -> bool:
        try:
            self.connection
            return True
        except rethinkdb.errors.ReqlDriverError as exc:
            pass
        return False
