#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# GNU GPLv3 <https://www.gnu.org/licenses/gpl-3.0.en.html>


import time
import importlib

from .. import const, device
from ..models import Record, RecordPoint
from ._common import AbstractTranslator

import bs4
import pint
import dateutil.parser


class ObviusTranslator(AbstractTranslator):
    """ The translator for Obvius devices.
    """

    supported_requesters = ('ObviusRequester',)
    _parser_pref = ['lxml', 'html.parser']
    _expression_unit_map = {
        # energy
        'kWh': 'kilowatthour',
        'Wh': 'watthour',
        'MWh': 'megawatthour',
        'VAh': 'volt_ampere * hour',
        'kVAh': 'kilovolt_ampere * hour',
        'MVAh': 'megavolt_ampere * hour',
        'VARh': 'volt_ampere * hour',
        'kVARh': 'kilovolt_ampere * hour',
        'MVARh': 'megavolt_ampere * hour',
        'Btu': 'btu',
        'kBtu': 'kilobtu',
        'MBtu': 'megabtu',
        'MMBtu': 'megabtu',
        'BtuE6': 'megabtu',
        'Ton-Hrs': 'ton * hour',
        'therms': 'thm',
        # power
        'W': 'watt',
        'mW': 'milliwatt',
        'kW': 'kilowatt',
        'MW': 'megawatt',
        'VA': 'volt_ampere',
        'kVA': 'kilovolt_ampere',
        'MVA': 'megavolt_ampere',
        'VAR': 'volt_ampere',
        'kVAR': 'kilovolt_ampere',
        'MVAR': 'megavolt_ampere',
        'Btu/hr': 'btu/hr',
        # voltage
        'Volts': 'volt',
        'mV': 'millivolt',
        'kV': 'kilovolt',
        'MV': 'megavolt',
        # current
        'Amps': 'amp',
        'mA': 'milliamp',
        # event counting
        'cycles': 'cycles',
        'pulses': '',
        'revolutions': 'revolution',
        'starts': '',
        # frequency
        'Hz': 'hertz',
        'kHz': 'kilohertz',
        'RPM': 'rpm',
        # resistance
        'Ohms': 'ohm',
        'kohms': 'kiloohm',
        # mass
        'kgs': 'kilogram',
        'Lbs': 'pound',
        'Tons': 'ton',
        # mass flow
        'kg/hr': 'kilogram/hour',
        'Lb/hr': 'pound/hour',
        # volume
        'Gallons': 'gallon',
        'Cubic Feet': 'foot ** 3',
        'Cubic Meters': 'meter ** 3',
        'Liters': 'liter',
        # volume flow
        'Cubic Feet/sec': 'foot ** 3/second',
        'Cubic Feet/min': 'foot ** 3/minute',
        'CFm': 'foot ** 3/minute',
        'CFM': 'foot ** 3/minute',
        'Cubic Feet/hr': 'foot ** 3/hour',
        'CFH': 'foot ** 3/hour',
        'Cubic Meters/hr': 'meter ** 3 / hour',
        'Gpm': 'gallon/minute',
        'Gph': 'gallon/hour',
        'MGD': 'megagallon/day',
        'Liters/sec': 'liter/second',
        'Liters/min': 'liter/minute',
        'Liters/hr': 'liter/hour',
        # velocity
        'MPH': 'mph',
        'KPH': 'kph',
        # temperature
        'Degrees C': 'degC',
        'Degrees F': 'degF',
        'C': 'degC',
        'F': 'degF',
        # humidity
        '%RH': '',
        # phase
        'Degrees': 'degree',
        # electrical
        'PF': '',
        'aPF': '',
        'dPF': '',
        # intensity
        'W/m^2': 'watt / meter ** 2',
        # dimensionless
        '%': '',
        'PPM': '',
        '': '',
        # time
        'days': 'day',
        'hours': 'hour',
        'minutes': 'minute',
        'seconds': 'second',
        'ms': 'millisecond',
        # pressure
        'Pa': 'pascal',
        'kPa': 'kilopascal',
        'inWC': '',
        'inAq': '',
        'inHg': 'inHg',
        'cmHg': 'cmHg',
        'mmHg': 'mmHg',
    }

    def __init__(self):
        """ Initiaalizes the Obvius translator.
        """

        self._unit_reg = pint.UnitRegistry(autoconvert_offset_to_baseunit=True)

    @property
    def parser(self) -> str:
        """ The `xml` parser to use for parsing the returned requester content.
        """

        if not hasattr(self, '_parser') or \
                self._parser not in self._parser_pref:
            for parser in self._parser_pref:
                if importlib.util.find_spec(parser):
                    self._parser = parser
                    break
        return self._parser

    @property
    def unit_map(self) -> dict:
        """ The mapping of Obvius units to valid pint units.
        """

        if not hasattr(self, '_unit_map'):
            self._unit_map = {}
            for (k, v) in self._expression_unit_map.items():
                self._unit_map[k] = self._unit_reg.parse_expression(v)
        return self._unit_map

    def validate(self, data: str) -> bool:
        """ Checks if the data from the Obvius is valid.

        :param data: The data returned from a supported requester
        :type data: str
        :returns: True if the data is valid, otherwise False
        :rtype: bool
        """

        return int(
            bs4.BeautifulSoup(data, self.parser)
            .find('error').text
        ) == 0

    def translate(self, data: str, meta: dict={}) -> None:
        """ Translates Obvius data to a record.

        :param data: The xml returned from the Obvius endpoint
        :type data: str
        :param meta: Any additional data given to the requester
        :type meta: dict
        :returns: Does not return
        :rtype: None
        """

        if self.validate(data):
            soup = bs4.BeautifulSoup(data, self.parser)
            for device_record in soup.find_all('devices'):
                # prepopulate the Record with meta fields that match
                record = Record(**meta)
                if not record.type or len(record.type) <= 0:
                    const.log.warning((
                        'no device type for `{record}`, '
                        'default set to {device.DeviceType.UNKNOWN} ...'
                    ).format(record=record, device=device))
                    record.type = device.DeviceType.UNKNOWN.name
                try:
                    # discover device type
                    device_type = device.DeviceType[record.type]
                    record.device_name = device_record.find('name').text
                    for rec in device_record.find_all('record'):
                        record.timestamp = time.time()
                        rec_error = rec.find('error').text
                        record_data = {}
                        for point in sorted(
                            rec.find_all('point'),
                            key=lambda x: int(x.attrs['number'])
                        ):
                            # discover valid point values and units
                            try:
                                rec_point_value = float(point.attrs['value'])
                            except ValueError:
                                rec_point_value = None
                            try:
                                self.unit_map[point.attrs['units']]
                            except KeyError:
                                point.attrs['units'] = ''

                            # add generated RecordPoint to record_data
                            record_data[
                                int(point.attrs['number'])
                            ] = RecordPoint(
                                name=point.attrs['name'],
                                value=rec_point_value,
                                unit=str(self.unit_map[
                                    point.attrs['units']
                                ].units)
                            )

                        # try and parse record data into reliable parsed data
                        record.data = record_data
                        (device_type_id, device_instance,) = device_type.value
                        record.parsed = device_instance.parse(record)
                    # send the generated record out to the engine
                    self.signal.send(record)
                except KeyError as exc:
                    const.log.error((
                        'invalid device type `{exc.args[0]}` for '
                        'record `{record}`, discarding record ...'
                    ).format(exc=exc, record=record))
                    break
