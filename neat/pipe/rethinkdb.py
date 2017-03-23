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
from typing import List

from .. import const
from ..models import Record
from ._common import AbstractPipe

import rethinkdb


class RethinkDBPipe(AbstractPipe):

    def __init__(
        self, rethink_ip: str, rethink_port: int, rethink_table: str,
        record_size: int=10
    ):
        (self._rethink_ip, self._rethink_port) = (rethink_ip, rethink_port)
        self._rethink_table = rethink_table
        (self._record_list, self._record_size,) = ([], record_size,)

        if self._rethink_table not in rethinkdb.table_list()\
                .run(self.connection):
            rethinkdb.table_create(self._rethink_table).run(self.connection)
        self.table = rethinkdb.table(self._rethink_table)

    def __repr__(self):
        return ((
            '<{self.__class__.__name__} '
            '({self._rethink_ip}:{self._rethink_port})>'
        ).format(self=self))

    @property
    def connection(self):
        # NOTE: unfortunately rethinkdb driver connections are not thread safe
        # For this reason, a new connection must be initalized on each request
        try:
            connection = rethinkdb.connect(
                self._rethink_ip, self._rethink_port,
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
                '`{self._rethink_ip}:{self._rethink_port}`, '
                '{exc.message} ...'
            ).format(self=self, exc=exc))
            raise exc

    def accept(self, record: Record) -> None:
        self.commit([record])

    def validate(self) -> bool:
        try:
            self.connection
            return True
        except rethinkdb.errors.ReqlDriverError as exc:
            pass
        return False

    def commit(self, records: List[Record]) -> None:
        const.log.debug((
            'commiting `{records_len}` records into rethinkdb `{self}` ...'
        ).format(self=self, records_len=len(records)))
        self.table.insert([record.to_dict() for record in records])\
            .run(self.connection)
