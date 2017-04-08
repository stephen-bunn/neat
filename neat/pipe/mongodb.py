#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn <r>
# GNU GPLv3 <https://www.gnu.org/licenses/gpl-3.0.en.html>

"""
mongodb.py
.. module::
    :platform: Linux, MacOSX, Win32
    :synopsis:
    :modified: 04-08-2017 16:13:23
.. moduleauthor:: Stephen Bunn <r>
"""

from .. import const
from ..models import Record
from ._common import AbstractPipe

import pymongo


class MongoDBPipe(AbstractPipe):

    def __init__(self, ip: str, port: int, table: str):
        (self._ip, self._port) = (ip, port)
        self._table_name = table

    def __repr__(self):
        return ((
            '<{self.__class__.__name__} '
            '({self._mongo_ip}:{self._mongo_port})>'
        ).format(self=self))

    @property
    def client(self) -> pymongo.MongoClient:
        if not hasattr(self, '_client'):
            try:
                self._client = pymongo.MongoClient(self._ip, self._port)
            except pymongo.errors.ConnectionFailure as exc:
                const.log.error((
                    'could not connect to mongodb server at '
                    '`{self._ip}:{self._port}`, {exc.message} ...'
                ).format(self=self))
                raise exc
        return self._client

    @property
    def db(self):
        if not hasattr(self, '_db'):
            self._db = self.client[const.module_name]
        return self._db

    @property
    def table(self):
        if not hasattr(self, '_table'):
            self._table = self.db.collection[self._table_name]
        return self._table

    def accept(self, record: Record) -> None:
        const.log.debug((
            'commiting `{record}` records into `{self}` ...'
        ).format(self=self, record=record))
        self.table.insert_one(record.to_dict())
        self.signal.send(self, record=record)

    def validate(self) -> bool:
        try:
            self.connection
            return True
        except pymongo.errors.ConnectionFailure as exc:
            pass
        return False
