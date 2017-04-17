#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# GNU GPLv3 <https://www.gnu.org/licenses/gpl-3.0.en.html>

from typing import List, Dict

from .. import const
from ._common import AbstractModel

import pint
import jsonschema


class RecordPoint(object):
    """ A record point representation.

    .. note:: Not a subclass of :class:`neat.models._common.AbstractModel`
    """

    def __init__(self, **kwargs):
        """ Initializes the record point with any preliminary fields.

        :param kwargs: A dictionary of any preliminary fields
        :type kwargs: dict
        """

        self._meta = {}
        for (k, v) in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)
            else:
                self._meta[k] = v

    @property
    def number(self) -> int:
        """ The number of the record point.
        """

        if hasattr(self, '_number'):
            return self._number

    @number.setter
    def number(self, number: int) -> None:
        """ Sets the number of the record point.

        :param number: The new number of the record point
        :type number: int
        """

        self._number = number

    @property
    def name(self) -> str:
        """ The name of the record point.
        """

        if hasattr(self, '_name'):
            return self._name

    @name.setter
    def name(self, name: str) -> None:
        """ Sets the name of the record point.

        :param name: The new name of the record point
        :type name: str
        """

        self._name = name

    @property
    def unit(self) -> str:
        """ The pint unit expression of the record point.
        """

        if hasattr(self, '_unit'):
            return self._unit

    @unit.setter
    def unit(self, unit: str) -> None:
        """ Sets the unit of the record point.

        :param unit: The new pint unit expression of the record point
        :type unit: str
        """

        self._unit = unit

    @property
    def value(self) -> float:
        """ The value of the record point.
        """

        if hasattr(self, '_value'):
            return self._value

    @value.setter
    def value(self, value: float) -> None:
        """ Sets the value of the record point.

        :param value: The new value of the record point
        :type value: float
        """

        self._value = value

    def to_dict(self) -> dict:
        """ Builds a serializable representation of the record point.

        :returns: A serializable representation of the record point
        :rtype: dict
        """

        data = {
            'value': self.value,
            'unit': self.unit
        }
        if hasattr(self, '_name'):
            data['name'] = self.name
        if hasattr(self, '_number'):
            data['number'] = self.number
        return data


class Record(AbstractModel):
    """ A model representation of a record.
    """

    def __init__(self, **kwargs):
        """ Initializes the record with any preliminary fields.

        :param kwargs: A dictionary of any preliminary fields
        :type kwargs: dict
        """

        (self._data, self._parsed, self._meta,) = ({}, {}, {},)
        for (k, v) in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)
            else:
                self._meta[k] = v

    def __repr__(self):
        """ A string representation of the record.

        :returns: A string representation of the record
        :rtype: str
        """

        return (
            '<{self.__class__.__name__} ({self.timestamp}) "{self.name}">'
        ).format(self=self)

    @property
    def device_name(self) -> str:
        """ The human readable name of the device.
        """

        if hasattr(self, '_device_name'):
            return self._device_name

    @device_name.setter
    def device_name(self, device_name: str) -> None:
        """ Sets the human readable name of the device.

        :param device_name: The new human readable device name
        :type device_name: str
        """

        self._device_name = device_name

    @property
    def name(self) -> str:
        """ The primary name of the device.
        """

        if hasattr(self, '_name'):
            return self._name

    @name.setter
    def name(self, name: str) -> None:
        """ Sets the primary name of the device.

        :param name: The new primary name of the device
        :type name: str
        """

        self._name = name

    @property
    def lon(self) -> float:
        """ The longitude of the device.
        """

        if hasattr(self, '_lon'):
            return self._lon

    @lon.setter
    def lon(self, lon: float) -> None:
        """ Sets the longitude of the record's device.

        :param lon: The new longitude of the record's device
        :type long: float
        """

        self._lon = float(lon)

    @property
    def lat(self) -> float:
        """ The latitude of the device.
        """

        if hasattr(self, '_lat'):
            return self._lat

    @lat.setter
    def lat(self, lat: float) -> None:
        """ Sets the latitude of the record's device.

        :param lon: The new latitude of the record's device
        :type long: float
        """

        self._lat = float(lat)

    @property
    def timestamp(self) -> int:
        """ The record's creation unix timestamp.
        """

        if hasattr(self, '_timestamp'):
            return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp: int) -> None:
        """ Sets the unix timestamp of the record.

        :param timestamp: The new unix timestamp of the record
        :type timestamp: int
        """

        self._timestamp = int(timestamp)

    @property
    def ttl(self) -> int:
        """ The record's time to live in seconds.
        """

        if hasattr(self, '_ttl'):
            return self._ttl

    @ttl.setter
    def ttl(self, ttl: int) -> None:
        """ Sets the time to live of the record.

        :param ttl: The new time to live of the record
        :type ttl: int
        """

        self._ttl = int(ttl)

    @property
    def type(self) -> str:
        """ The type of the device.
        """

        if hasattr(self, '_device_type'):
            return self._device_type

    @type.setter
    def type(self, device_type: str) -> None:
        """ Sets the type of the device.

        :param device_type: A string of the key matching the DeviceType enum
        :type device_type: str
        """

        self._device_type = device_type

    @property
    def data(self) -> Dict[int, RecordPoint]:
        """ The device's raw data points.
        """

        if hasattr(self, '_data'):
            return self._data

    @data.setter
    def data(self, data: Dict[int, RecordPoint]) -> None:
        """ Sets the data of the device.

        :param data: A dictionary of device points to RecordPoints
        :type data: dict
        """

        self._data = data

    @property
    def parsed(self) -> Dict[str, RecordPoint]:
        """ The device's parsed data points.
        """

        if hasattr(self, '_parsed'):
            return self._parsed

    @parsed.setter
    def parsed(self, parsed: Dict[str, RecordPoint]) -> None:
        """ Sets the parsed data points.

        :param parsed: A dictionary of the parsed data points
        :type parsed: dict
        """

        self._parsed = parsed

    def validate(self) -> bool:
        """ Self validates the record.

        :returns: True if valid, otherwise False
        :rtype: bool
        """

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
        """ Builds a serializable representation of the record.

        :returns: A serializable representation of the record
        :rtype: dict
        """

        return {
            'name': self.name,
            'device_name': self.device_name,
            'type': self.type,
            'timestamp': self.timestamp,
            'data': {
                str(point_number): record_point.to_dict()
                for (point_number, record_point) in self.data.items()
            },
            'parsed': {
                point_name: record_point.to_dict()
                for (point_name, record_point) in self.parsed.items()
            },
            'coord': {
                'lon': self.lon,
                'lat': self.lat
            },
            'ttl': self.ttl,
            'meta': self._meta
        }
