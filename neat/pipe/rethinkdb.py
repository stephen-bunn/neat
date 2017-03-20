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

    def __init__(self, rethink_ip: str, rethink_port: int, rethink_table: str):
        (self._rethink_ip, self._rethink_port) = (rethink_ip, rethink_port)
        self._rethink_table = rethink_table

    def __repr__(self):
        return ((
            '<{self.__class__.__name__} '
            '({self._rethink_ip}:{self._rethink_port})>'
        ).format(self=self))

    @property
    def connection(self):
        if not hasattr(self, '_connection'):
            const.log.info((
                'initializing connection to rethink database at '
                '`{self._rethink_ip}:{self._rethink_port}` ...'
            ).format(self=self))
            try:
                self._connection = rethinkdb.connect(
                    self._rethink_ip, self._rethink_port,
                    db=const.module_name
                )
                if const.module_name not in rethinkdb.db_list()\
                        .run(self._connection):
                    rethinkdb.db_create(const.module_name)\
                        .run(self._connection)
            except rethinkdb.errors.ReqlDriverError as exc:
                const.log.error((
                    'could not connect to rethinkdb server at '
                    '`{self._rethink_ip}:{self._rethink_port}`, '
                    '{exc.message} ...'
                ).format(self=self, exc=exc))
                raise exc
        return self._connection

    @property
    def table(self):
        if not hasattr(self, '_table'):
            if self._rethink_table not in rethinkdb.table_list()\
                    .run(self.connection):
                rethinkdb.table_create(self._rethink_table)\
                    .run(self.connection)
            self._table = rethinkdb.table(self._rethink_table)
        return self._table

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
        self.signal.send(self)
