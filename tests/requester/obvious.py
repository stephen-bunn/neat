#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn <r>
# GNU GPLv3 <https://www.gnu.org/licenses/gpl-3.0.en.html>

"""
obvious.py
.. module:: neat
    :platform: Linux, MacOSX, Win32
    :synopsis:
    :created: 02-17-2017 12:34:38
    :modified: 02-17-2017 12:34:38
.. moduleauthor:: Stephen Bunn <r>
"""

import struct
import random
import socket
import unittest

from neat.requester.obvious import ObviousRequester

import blinker
import requests_mock


class ObviousRequesterTest(unittest.TestCase):

    def setUp(self):
        self._req = ObviousRequester(1, '127.0.0.1', 'user', 'pass')
        self._req_url = (
            'http://{req._obvious_ip}:{req._obvious_port}'
            '{req._request_endpoint}?ADDRESS={req._device_id}&TYPE=DATA'
        ).format(req=self._req)

    def tearDown(self):
        del self._req

    def test_initialization(self):
        with self.assertRaises(TypeError):
            ObviousRequester()

        req = ObviousRequester(None, None, None, None)
        self.assertIsNone(req.device_id)
        self.assertIsNone(req._obvious_ip)
        self.assertIsNone(req._obvious_user)
        self.assertIsNone(req._obvious_pass)
        self.assertEqual(req._obvious_port, 80)

        req = ObviousRequester(1, '127.0.0.1', 'user', 'pass', 93)
        self.assertEqual(req.device_id, 1)
        self.assertEqual(req._obvious_ip, '127.0.0.1')
        self.assertEqual(req._obvious_user, 'user')
        self.assertEqual(req._obvious_pass, 'pass')
        self.assertEqual(req._obvious_port, 93)
        del req

    def test_signal_name(self):
        self.assertEqual(
            self._req.signal_name,
            'ObviousRequester_127.0.0.1:80_1'
        )

    def test_signal(self):
        self.assertIsInstance(self._req.signal, blinker.Signal)

    def test_request_receive(self):
        that = self

        @self._req.signal.connect
        def _receiver(requester, data):
            that.assertIsInstance(requester, ObviousRequester)
            that.assertEqual(data, 'data')

        with requests_mock.mock() as mock:
            mock.get(
                self._req_url,
                text='data'
            )
            self.assertIsNone(self._req.request())
