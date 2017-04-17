#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# GNU GPLv3 <https://www.gnu.org/licenses/gpl-3.0.en.html>

import enum
import logging
import unittest

from neat import const
from neat.models.record import Record, RecordPoint
from neat.device import AbstractDevice, DeviceType

import pint


class DeviceTypeTest(unittest.TestCase):

    def setUp(self):
        const.log_level = logging.CRITICAL
        self._device_type = DeviceType
        self._valid_test_record = Record(**{
            'device_name': 'test_device_name',
            'name': 'test_name',
            'lon': 12.3,
            'lat': -12.3,
            'timestamp': 1234567890,
            'ttl': 1,
            'type': 'WIND',
            'data': {
                '0': RecordPoint(**{
                    'name': 'test_inverter_real',
                    'unit': 'kilowatt',
                    'value': 123.45
                }),
                '1': RecordPoint(**{
                    'name': 'test_energy_total',
                    'unit': 'kilowatthour',
                    'value': 123.45
                }),
                '2': RecordPoint(**{
                    'name': 'test_rotor_speed',
                    'unit': 'rpm',
                    'value': 123.45
                }),
                '3': RecordPoint(**{
                    'name': 'test_wind_speed',
                    'unit': 'mph',
                    'value': 123.45
                })
            },
            'parsed': {
                'inverter_real': {
                    'point': '0',
                    'unit': 'kilowatt'
                },
                'inverter_energy_total': {
                    'point': '1',
                    'unit': 'kilowatthour'
                },
                'rotor_speed': {
                    'point': '2',
                    'unit': 'rpm'
                },
                'wind_speed': {
                    'point': '3',
                    'unit': 'mph'
                }
            }
        })
        self._invalid_test_record = Record(**{
            'device_name': 'test_device_name',
            'name': 'test_name',
            'lon': 12.3,
            'lat': -12.3,
            'timestamp': 1234567890,
            'ttl': 1,
            'type': 'UNKNOWN',
            'data': {
                '0': RecordPoint(**{
                    'name': 'test_inverter_real',
                    'unit': 'kilowatt',
                    'value': 123.45
                }),
                '1': RecordPoint(**{
                    'name': 'test_energy_total',
                    'unit': 'kilowatthour',
                    'value': 123.45
                }),
                '2': RecordPoint(**{
                    'name': 'test_rotor_speed',
                    'unit': 'rpm',
                    'value': 123.45
                }),
                '3': RecordPoint(**{
                    'name': 'test_wind_speed',
                    'unit': 'mph',
                    'value': 123.45
                })
            },
            'parsed': {
                'inverter_real': {
                    'point': '0',
                    'unit': 'kilowatt'
                },
                'inverter_energy_total': {
                    'point': '1',
                    'unit': 'kilowatthour'
                },
                'rotor_speed': {
                    'point': '2',
                    'unit': 'rpm'
                },
                'wind_speed': {
                    'point': '3',
                    'unit': 'mph'
                }
            }
        })
        self._broken_test_record = Record(**{
            'device_name': 'test_device_name',
            'name': 'test_name',
            'lon': 12.3,
            'lat': -12.3,
            'timestamp': 1234567890,
            'ttl': 1,
            'type': 'WIND',
            'data': {
                '0': RecordPoint(**{
                    'name': 'test_inverter_real',
                    'unit': 'kilowatt',
                    'value': 123.45
                }),
                '1': RecordPoint(**{
                    'name': 'test_energy_total',
                    'unit': 'kilowatthour',
                    'value': 123.45
                }),
                '2': RecordPoint(**{
                    'name': 'test_rotor_speed',
                    'unit': 'rpm',
                    'value': 123.45
                }),
                '3': RecordPoint(**{
                    'name': 'test_wind_speed',
                    'unit': 'mph',
                    'value': 123.45
                })
            },
            'parsed': {
                'test_broken': {
                    'point': '0',
                    'unit': 'kilowatt'
                },
                'inverter_energy_total': {
                    'point': '1',
                    'unit': 'kilowatthour'
                },
                'rotor_speed': {
                    'point': '2',
                    'unit': 'rpm'
                },
                'wind_speed': {
                    'point': '3',
                    'unit': 'mph'
                }
            }
        })

    def tearDown(self):
        del self._device_type
        del self._valid_test_record
        del self._invalid_test_record

    def test_device_enum(self):
        self.assertNotIsInstance(self._device_type, enum.Enum)
        for entry in self._device_type:
            self.assertIsInstance(entry.value, tuple)
            self.assertEqual(len(entry.value), 2)
            self.assertIsInstance(entry.value[-1], AbstractDevice)
            self.assertIsInstance(entry.value[-1].ureg, pint.UnitRegistry)

    def test_parse(self):
        valid_parsed = self._device_type[
            self._valid_test_record.type
        ].value[-1].parse(self._valid_test_record)
        self.assertIsInstance(valid_parsed, dict)

        invalid_parsed = self._device_type[
            self._invalid_test_record.type
        ].value[-1].parse(self._invalid_test_record)
        self.assertIsInstance(invalid_parsed, dict)
        self.assertEqual(invalid_parsed, {})

        broken_parsed = self._device_type[
            self._broken_test_record.type
        ].value[-1].parse(self._broken_test_record)
        self.assertIsInstance(broken_parsed, dict)
        self.assertNotIn('test_broken', broken_parsed.keys())
        self.assertIsInstance(broken_parsed['inverter_real'], RecordPoint)
        self.assertIsNone(broken_parsed['inverter_real'].value)
        self.assertEqual(broken_parsed['inverter_real'].unit, 'dimensionless')
