#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn <r>
# GNU GPLv3 <https://www.gnu.org/licenses/gpl-3.0.en.html>

"""
device.py
    :platform: Linux, MacOSX, Win32
    :synopsis:
    :created: 03-13-2017 19:18:22
    :modified: 03-13-2017 19:18:22
.. moduleauthor:: Stephen Bunn <r>
"""

import abc
import enum
from typing import Dict

from . import const
from .models.record import Record, RecordPoint

import pint


class AbstractDevice(object, metaclass=abc.ABCMeta):

    @abc.abstractproperty
    def name(self) -> str:
        raise NotImplementedError()

    @abc.abstractproperty
    def fields(self) -> Dict[str, str]:
        raise NotImplementedError()

    @property
    def ureg(self) -> pint.UnitRegistry:
        if not hasattr(self, '_ureg'):
            self._ureg = pint.UnitRegistry(autoconvert_offset_to_baseunit=True)
        return self._ureg

    def parse(self, record: Record) -> Dict[str, RecordPoint]:
        record_parsed = {}
        if isinstance(record.parsed, dict) and \
                not isinstance(self, UnknownDevice):
            for (parsed_name, parsed_config) in record.parsed.items():
                record_point = record.data[parsed_config['number']]
                parsed_point = (self.ureg.Quantity(
                    record_point.value, self.ureg.Unit(record_point.unit)
                )).to(self.ureg.Unit(self.fields[parsed_name]))
                record_parsed[parsed_name] = RecordPoint(
                    value=parsed_point.magnitude,
                    unit=str(parsed_point.units)
                )
            for (req_name, req_unit) in self.fields.items():
                try:
                    record_parsed[req_name]
                except KeyError as exc:
                    const.log.warning((
                        'missing required specification for parsed field '
                        '`{req_name}`, setting to empty record point ...'
                    ).format(req_name=req_name))
                    record_parsed[req_name] = RecordPoint(
                        value=None, unit='dimensionless'
                    )
        return record_parsed


class UnknownDevice(AbstractDevice):
    name = 'Unknown Device'
    fields = {}


class PVDevice(AbstractDevice):
    name = 'PV Device'
    fields = {}


class HVACDevice(AbstractDevice):
    name = 'HVAC Device'
    fields = {}


class SolarThermalDevice(AbstractDevice):
    name = 'Solar Thermal Device'
    fields = {}


class WindDevice(AbstractDevice):
    name = 'Wind Device'
    fields = {
        'rotor_speed': 'rpm',
        'wind_speed': 'mph'
    }


class FlowDevice(AbstractDevice):
    name = 'Flow Device'
    fields = {
        'energy_rate': 'btu / hour',
        'flow_rate': 'gallon / minute',
        'supply_temp': 'degF',
        'return_temp': 'degF'
    }


class EnergyDevice(AbstractDevice):
    name = 'Energy Device'
    fields = {}


class TemperatureDevice(AbstractDevice):
    name = 'Temperature Device'
    fields = {}


class DeviceType(enum.Enum):
    """ An enumeration of available device types.
    """

    UNKNOWN     = (0x0, UnknownDevice())
    PV          = (0x1, PVDevice())
    HVAC        = (0x2, HVACDevice())
    SOLAR_THERM = (0x3, SolarThermalDevice())
    WIND        = (0x4, WindDevice())
    FLOW        = (0x5, FlowDevice())
    ENERGY      = (0x6, EnergyDevice())
    TEMP        = (0x7, TemperatureDevice())
