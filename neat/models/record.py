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

import jsonschema
from typing import List

from .. import const

import pint


class RecordPoint(object):

        def __init__(self, **kwargs):
            self._meta = kwargs

        @property
        def name(self) -> str:
            return self._name

        @name.setter
        def name(self, name: str) -> None:
            self._name = name

        @property
        def unit(self):
            return self._unit

        @unit.setter
        def unit(self, unit) -> None:
            self._unit = unit

        @property
        def value(self) -> float:
            return self._value

        @value.setter
        def value(self, value: float) -> None:
            self._value = value

        def to_json(self) -> dict:
            return {
                'name': self.name,
                'value': self.value,
                'unit': self.unit
            }


class Record(object):

    def __init__(self, **kwargs):
        self._meta = kwargs
        (self._data, self._parsed,) = ([], [])

    @property
    def device_name(self) -> str:
        if hasattr(self, '_device_name'):
            return self._device_name
        return None

    @device_name.setter
    def device_name(self, device_name: str) -> None:
        self._device_name = device_name

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @property
    def longitude(self) -> float:
        if hasattr(self, '_longitude'):
            return self._longitude
        return None

    @longitude.setter
    def longitude(self, longitude: float) -> None:
        self._longitude = longitude

    @property
    def latitude(self) -> float:
        if hasattr(self, '_latitude'):
            return self._latitude
        return None

    @latitude.setter
    def latitude(self, latitude: float) -> None:
        self._latitude = latitude

    @property
    def timestamp(self) -> int:
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp: int) -> None:
        self._timestamp = timestamp

    @property
    def device_type(self):
        if hasattr(self, '_device_type'):
            return self._device_type
        return None

    @device_type.setter
    def device_type(self, device_type) -> None:
        self._device_type = device_type

    @property
    def data(self) -> List[RecordPoint]:
        return self._data

    @property
    def parsed(self) -> List[RecordPoint]:
        return self._parsed

    @property
    def valid(self) -> bool:
        try:
            jsonschema.validate(self.to_json(), const.record_schema)
            return True
        except jsonschema.exceptions.ValidationError as exc:
            return False

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'device_name': self.device_name,
            'device_type': self.device_type,
            'timestamp': self.timestamp,
            'data': [point.to_json() for point in self.data],
            'parsed': [point.to_json() for point self.parsed],
            'coord': {
                'long': self.longitude,
                'lat': self.latitude
            },
            'meta': self._meta
        }
