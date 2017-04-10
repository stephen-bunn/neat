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

import time

from .. import const
from ..models import Record
from ._common import AbstractPipe

import pymongo


class MongoDBPipe(AbstractPipe):

    def __init__(self, ip: str, port: int, table: str, entry_delay: int=600):
        (self._ip, self._port) = (ip, port)
        self._table_name = table
        (self._entry_register, self._entry_delay) = ({}, entry_delay)

    def __repr__(self):
        return ((
            '<{self.__class__.__name__} ({self._ip}:{self._port})>'
        ).format(self=self))

    @property
    def client(self) -> pymongo.MongoClient:
        if not hasattr(self, '_client'):
            try:
                self._client = pymongo.MongoClient(
                    self._ip, self._port, connect=False
                )
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
            'handling `{record}` with `{self}` ...'
        ).format(self=self, record=record))
        last_write = time.time()
        insert = False
        try:
            last_write = (time.time() - self._entry_register[record.name])
            if last_write >= self._entry_delay:
                insert = True
        except KeyError as exc:
            self._entry_register[record.name] = time.time()
            insert = True
        if insert:
            const.log.debug((
                'commiting `{record}` records into `{self}` ...'
            ).format(self=self, record=record))
            self.table.insert_one({
                (k[1:] if k.startswith('$') else k): v
                for (k, v) in record.to_dict().items()
            })
        else:
            const.log.debug((
                'dropping `{record}` for `{self}`, time till next write is '
                '`{next_write}` seconds ...'
            ).format(
                self=self, record=record,
                next_write=(self._entry_delay - last_write)
            ))
        self.signal.send(self, record=record)

    def validate(self) -> bool:
        try:
            self.client
            return True
        except pymongo.errors.ConnectionFailure as exc:
            pass
        return False
