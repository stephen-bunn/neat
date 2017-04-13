#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# GNU GPLv3 <https://www.gnu.org/licenses/gpl-3.0.en.html>

import time

from .. import const
from ..models import Record
from ._common import AbstractPipe

import pymongo


class MongoDBPipe(AbstractPipe):
    """ A record pipe for MongoDB.

    .. note:: Records are always placed in the `neat` table.
    """

    def __init__(self, ip: str, port: int, table: str, entry_delay: int=600):
        """ Initializes the MongoDB pipe.

        :param ip: The IP of the MongoDB instance
        :type ip: str
        :param port: The port of the MongoDB instance
        :type port: int
        :param table: The table name of the table to place records into
        :type table: str
        :param entry_delay: Seconds between allowing records into the database
        :type entry_delay: int
        """

        (self._ip, self._port) = (ip, port)
        self._table_name = table
        (self._entry_register, self._entry_delay) = ({}, entry_delay)

    def __repr__(self):
        """ A string representation of the pipe.

        :returns: A string representation of the pipe
        :rtype: str
        """

        return ((
            '<{self.__class__.__name__} ({self._ip}:{self._port})>'
        ).format(self=self))

    @property
    def client(self) -> pymongo.MongoClient:
        """ The client attached to the MongoDB uri.

        .. warning:: MongoDB driver connections are not fork safe
        """

        # NOTE: since mongodb driver connections are not fork safe, setting
        # connect to False is required
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
        """ The database of the client to write to.
        """

        if not hasattr(self, '_db'):
            self._db = self.client[const.module_name]
        return self._db

    @property
    def table(self):
        """ The table of the database to write to.
        """

        if not hasattr(self, '_table'):
            self._table = self.db.collection[self._table_name]
        return self._table

    def accept(self, record: Record) -> None:
        """ Accepts a record to be placed into the MongoDB instance.

        :param record: The record to be placed in the MongoDB instance
        :type record: Record
        :returns: Does not return
        :rtype: None
        """

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
                (k.replace('$', '') if k.startswith('$') else k): v
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
        """ Self validates the MongoDB pipe.

        :returns: True if the pipe is valid, otherwise False
        :rtype: bool
        """

        try:
            self.client
            return True
        except pymongo.errors.ConnectionFailure as exc:
            pass
        return False
