#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# GNU GPLv3 <https://www.gnu.org/licenses/gpl-3.0.en.html>

import logging
import unittest
from unittest.mock import MagicMock

from neat import const
from neat.requester.obvius import ObviusRequester

import blinker
import requests_mock


class ObviusRequesterTest(unittest.TestCase):

    def setUp(self):
        const.log_level = logging.CRITICAL
        self._req = ObviusRequester(
            1, '127.0.0.1', 'user', 'pass',
            test='meta'
        )
        self._req_url = (
            'http://{req._obvius_ip}:{req._obvius_port}'
            '{req._request_endpoint}?ADDRESS={req._device_id}&TYPE=DATA'
        ).format(req=self._req)

    def tearDown(self):
        del self._req

    def test_initialization(self):
        with self.assertRaises(TypeError):
            ObviusRequester()

        req = ObviusRequester(None, None, None, None)
        self.assertIsNone(req._device_id)
        self.assertIsNone(req._obvius_ip)
        self.assertIsNone(req._obvius_user)
        self.assertIsNone(req._obvius_pass)
        self.assertEqual(req._obvius_port, 80)

        req = ObviusRequester(1, '127.0.0.1', 'user', 'pass', 93)
        self.assertEqual(req._device_id, 1)
        self.assertEqual(req._obvius_ip, '127.0.0.1')
        self.assertEqual(req._obvius_user, 'user')
        self.assertEqual(req._obvius_pass, 'pass')
        self.assertEqual(req._obvius_port, 93)
        del req

    def test_signal(self):
        self.assertIsInstance(self._req.signal, blinker.Signal)

    def test_request_receive(self):
        that = self

        @self._req.signal.connect
        def _receiver(requester, data, meta):
            that.assertIsInstance(requester, ObviusRequester)
            that.assertEqual(data, 'data')
            that.assertEqual(meta, {'test': 'meta'})

        with requests_mock.mock() as mock:
            mock.get(self._req_url, text='data')

            self._req.signal.send = MagicMock()
            self.assertIsNone(self._req.request())
            self._req.signal.send.assert_called_with(
                self._req,
                data='data', meta={'test': 'meta'}
            )
