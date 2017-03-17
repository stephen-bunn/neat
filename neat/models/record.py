#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn <r>
# GNU GPLv3 <https://www.gnu.org/licenses/gpl-3.0.en.html>

"""
record.py
    :platform: Linux, MacOSX, Win32
    :synopsis:
    :created: 03-07-2017 16:05:02
    :modified: 03-07-2017 16:05:02
.. moduleauthor:: Stephen Bunn <r>
"""

from typing import List

from .. import const
from ._common import AbstractModel

import pint
import jsonschema


class RecordPoint(object):

    def __init__(self, **kwargs):
        self._meta = {}
        for (k, v) in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)
            else:
                self._meta[k] = v

    @property
    def name(self) -> str:
        if hasattr(self, '_name'):
            return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @property
    def unit(self):
        if hasattr(self, '_unit'):
            return self._unit

    @unit.setter
    def unit(self, unit) -> None:
        self._unit = unit

    @property
    def value(self) -> float:
        if hasattr(self, '_value'):
            return self._value

    @value.setter
    def value(self, value: float) -> None:
        self._value = value

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'value': self.value,
            'unit': self.unit
        }


class Record(AbstractModel):

    def __init__(self, **kwargs):
        (self._data, self._parsed, self._meta,) = ([], [], {},)
        for (k, v) in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)
            else:
                self._meta[k] = v

    def __repr__(self):
        return (
            '<{self.__class__.__name__} ({self.timestamp}) "{self.name}">'
        ).format(self=self)

    @property
    def device_name(self) -> str:
        if hasattr(self, '_device_name'):
            return self._device_name

    @device_name.setter
    def device_name(self, device_name: str) -> None:
        self._device_name = device_name

    @property
    def name(self) -> str:
        if hasattr(self, '_name'):
            return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @property
    def lon(self) -> float:
        if hasattr(self, '_lon'):
            return self._lon

    @lon.setter
    def lon(self, lon: float) -> None:
        self._lon = float(lon)

    @property
    def lat(self) -> float:
        if hasattr(self, '_lat'):
            return self._lat

    @lat.setter
    def lat(self, lat: float) -> None:
        self._lat = float(lat)

    @property
    def timestamp(self) -> int:
        if hasattr(self, '_timestamp'):
            return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp: int) -> None:
        self._timestamp = int(timestamp)

    @property
    def type(self):
        if hasattr(self, '_device_type'):
            return self._device_type

    @type.setter
    def type(self, device_type) -> None:
        self._device_type = device_type

    @property
    def data(self) -> List[RecordPoint]:
        if hasattr(self, '_data'):
            return self._data

    @data.setter
    def data(self, data: List[RecordPoint]) -> None:
        self._data = data

    @property
    def parsed(self) -> List[RecordPoint]:
        if hasattr(self, '_parsed'):
            return self._parsed

    @parsed.setter
    def parsed(self, parsed: List[RecordPoint]) -> None:
        self._parsed = parsed

    def validate(self) -> bool:
        try:
            jsonschema.validate(self.to_dict(), const.record_schema)
            return True
        except jsonschema.exceptions.ValidationError as exc:
            const.log.warn((
                'caught {self.__class__.__name__} validation error on the '
                'record `{to_dict}`, {exc} ...'
            ).format(self=self, to_dict=self.to_dict(), exc=str(exc)))
        return False

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'device_name': self.device_name,
            'type': self.type,
            'timestamp': self.timestamp,
            'data': [point.to_dict() for point in self.data],
            'parsed': [point.to_dict() for point in self.parsed],
            'coord': {
                'lon': self.lon,
                'lat': self.lat
            },
            '$meta': self._meta
        }
