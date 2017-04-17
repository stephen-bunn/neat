#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# GNU GPLv3 <https://www.gnu.org/licenses/gpl-3.0.en.html>

import abc
import enum
from typing import Dict

from . import const
from .models.record import Record, RecordPoint

import pint


class AbstractDevice(object, metaclass=abc.ABCMeta):
    """ The base class for all valid devices.
    """

    @abc.abstractproperty
    def name(self) -> str:
        """ The name of the device.
        """

        raise NotImplementedError()

    @abc.abstractproperty
    def fields(self) -> Dict[str, str]:
        """ The expected device fields.
        """

        raise NotImplementedError()

    @property
    def ureg(self) -> pint.UnitRegistry:
        """ The unit registry for all devices.
        """

        if not hasattr(self, '_ureg'):
            self._ureg = pint.UnitRegistry(autoconvert_offset_to_baseunit=True)
        return self._ureg

    def parse(self, record: Record) -> Dict[str, RecordPoint]:
        """ Parses a given record for the necessary device fields.

        :param record: The record to parse
        :type record: Record
        :returns: A dictionary of field names mapped to record points
        :rtype: dict
        """

        record_parsed = {}
        if isinstance(record.parsed, dict) and \
                not isinstance(self, UnknownDevice):
            for (parsed_name, parsed_config) in record.parsed.items():
                record_point = record.data[parsed_config['point']]
                try:
                    parsed_point = (self.ureg.Quantity(
                        record_point.value, self.ureg.Unit(record_point.unit)
                    )).to(self.ureg.Unit(self.fields[parsed_name]))
                    record_parsed[parsed_name] = RecordPoint(
                        value=parsed_point.magnitude,
                        unit=str(parsed_point.units)
                    )
                except KeyError as exc:
                    const.log.warning((
                        '`{record}` got unkown specification for a field '
                        '`{parsed_name}`, ignoring ...'
                    ).format(record=record, parsed_name=parsed_name))
            for (req_name, req_unit) in self.fields.items():
                try:
                    record_parsed[req_name]
                except KeyError as exc:
                    const.log.warning((
                        '`{record}` missing required specification for parsed '
                        'field `{req_name}`, setting to empty record point ...'
                    ).format(record=record, req_name=req_name))
                    record_parsed[req_name] = RecordPoint(
                        value=None, unit='dimensionless'
                    )
        return record_parsed


class UnknownDevice(AbstractDevice):
    """ Defines an unknown device type.

    .. note:: Primarily used for Obvius virtual meters
    """

    name = 'Unknown Device'
    fields = {}


class PVDevice(AbstractDevice):
    """ Defines a photovoltaic device.
    """

    name = 'PV Device'
    # TODO: determine default types for device
    fields = {}


class HVACDevice(AbstractDevice):
    """ Defines a heating, ventilation, and cooling device.
    """

    name = 'HVAC Device'
    # TODO: determine default types for device
    fields = {}


class SolarThermalDevice(AbstractDevice):
    """ Defines a solar thermal device.
    """

    name = 'Solar Thermal Device'
    fields = {
        'energy_rate': 'btu / hour',
        'flow_rate': 'gallon / minute',
        'supply_temp': 'degF',
        'return_temp': 'degF',
        'energy_total': 'megabtu'
    }


class WindDevice(AbstractDevice):
    """ Defines a wind based device.
    """

    name = 'Wind Device'
    fields = {
        'inverter_real': 'kilowatt',
        'inverter_energy_total': 'kilowatthour',
        'rotor_speed': 'rpm',
        'wind_speed': 'mph'
    }


class EnergyDevice(AbstractDevice):
    """ Defines a generic energy device.
    """

    name = 'Energy Device'
    # TODO: determine default types for device
    fields = {}


class TemperatureDevice(AbstractDevice):
    """ Defines a generic temperature device.
    """

    name = 'Temperature Device'
    # TODO: determine default types for device
    fields = {}


class DeviceType(enum.Enum):
    """ An enumeration of available device types.

    .. note:: Maps types to instances not classes
    """

    UNKNOWN     = (0x0, UnknownDevice())
    PV          = (0x1, PVDevice())
    HVAC        = (0x2, HVACDevice())
    SOLAR_THERM = (0x3, SolarThermalDevice())
    WIND        = (0x4, WindDevice())
    ENERGY      = (0x5, EnergyDevice())
    TEMP        = (0x6, TemperatureDevice())
