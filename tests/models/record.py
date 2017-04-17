#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# GNU GPLv3 <https://www.gnu.org/licenses/gpl-3.0.en.html>

import unittest

from neat import const
from neat.models.record import Record, RecordPoint


class RecordTest(unittest.TestCase):

    def setUp(self):
        self._blank_record = Record()
        self._populated_record = Record(**{
            'device_name': 'test_device_name',
            'name': 'test_name',
            'lon': 12.3,
            'lat': -12.3,
            'timestamp': 1234567890,
            'ttl': 1,
            'type': 'DEVICE_TYPE',
            'data': {
                '0': RecordPoint(**{
                    'number': 1,
                    'name': 'test_name',
                    'unit': 'test_unit',
                    'value': 123.45
                })
            }
        })

    def tearDown(self):
        del self._blank_record
        del self._populated_record

    def test_initialization(self):
        self.assertIsNone(self._blank_record.device_name)
        self.assertIsNone(self._blank_record.name)
        self.assertIsNone(self._blank_record.lon)
        self.assertIsNone(self._blank_record.lat)
        self.assertIsNone(self._blank_record.timestamp)
        self.assertIsNone(self._blank_record.ttl)
        self.assertIsNone(self._blank_record.type)
        self.assertEqual(self._blank_record.parsed, {})
        self.assertFalse(self._blank_record.validate())

        self.assertEqual(
            self._populated_record.device_name, 'test_device_name'
        )
        self.assertEqual(self._populated_record.name, 'test_name')
        self.assertEqual(self._populated_record.lon, 12.3)
        self.assertEqual(self._populated_record.lat, -12.3)
        self.assertEqual(self._populated_record.timestamp, 1234567890)
        self.assertEqual(self._populated_record.ttl, 1)
        self.assertEqual(self._populated_record.type, 'DEVICE_TYPE')
        self.assertIsInstance(self._populated_record.data, dict)
        self.assertIsInstance(self._populated_record.data['0'], RecordPoint)
        self.assertIsInstance(self._populated_record.parsed, dict)
        self.assertTrue(self._populated_record.validate())


class RecordPointTest(unittest.TestCase):

    def setUp(self):
        self._blank_record_point = RecordPoint()
        self._populated_record_point = RecordPoint(**{
            'number': 1,
            'name': 'test_name',
            'unit': 'test_unit',
            'value': 123.45
        })

    def tearDown(self):
        del self._blank_record_point

    def test_initialization(self):
        self.assertIsNone(self._blank_record_point.number)
        self.assertIsNone(self._blank_record_point.name)
        self.assertIsNone(self._blank_record_point.unit)
        self.assertIsNone(self._blank_record_point.value)
        self.assertEqual(
            self._blank_record_point.to_dict(),
            {'value': None, 'unit': None}
        )

        self.assertEqual(1, self._populated_record_point.number)
        self.assertEqual('test_name', self._populated_record_point.name)
        self.assertEqual('test_unit', self._populated_record_point.unit)
        self.assertEqual(123.45, self._populated_record_point.value)
        self.assertEqual(
            self._populated_record_point.to_dict(), {
                'number': 1, 'name': 'test_name',
                'unit': 'test_unit', 'value': 123.45
            }
        )
