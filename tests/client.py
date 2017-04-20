#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# GNU GPLv3 <https://www.gnu.org/licenses/gpl-3.0.en.html>

import os
import logging
import tempfile
import unittest
from unittest.mock import MagicMock

from neat import const
from neat.client import BasicClient

import yaml


class BasicClientTest(unittest.TestCase):

    def setUp(self):
        const.log_level = logging.CRITICAL
        self._test_config = '''---
        pipes:
          - $:           RethinkDBPipe
            ip:          localhost
            port:        28015
            table:       devices
            clean_delay: 300
          - $:           MongoDBPipe
            ip:          localhost
            port:        27017
            table:       devices
            entry_delay: 100
        devices:
          - scheduler:
              $:           SimpleDelayScheduler
              delay:       10.0
            requester:
              $:           ObviusRequester
              device_id:   18
              obvius_ip:   152.10.6.240
              obvius_port: 80
              obvius_user: test_user
              obvius_pass: test_pass
              name:        solar_therm.1
              type:        SOLAR_THERM
              lat:         -12.3
              lon:         12.3
              ttl:         300
              parsed:
                energy_total:
                  point: 5
                  unit:  btu
                energy_rate:
                  point: 0
                  unit:  btu / hour
                flow_rate:
                  point: 1
                  unit:  gallon / minute
                supply_temp:
                  point: 3
                  unit:  degF
                return_temp:
                  point: 4
                  unit:  degF
        '''
        self.client = BasicClient(yaml.load(self._test_config))

    def tearDown(self):
        del self.client

    def test_initialization(self):
        self.assertTrue(hasattr(self.client, 'engine'))

    def test_from_config(self):
        (fp_handle, fp_path) = tempfile.mkstemp()
        self.assertTrue(os.path.exists(fp_path))
        with open(fp_path, 'w') as fp:
            fp.write(self._test_config)
        client = BasicClient.from_config(fp_path)
        self.assertIsInstance(client, BasicClient)
        os.remove(fp_path)
        with self.assertRaises(FileNotFoundError):
            BasicClient.from_config('')

    def start(self):
        that = self

        @self.client.engine.on_start.connect
        def on_start_receiver(self, engine):
            that.assertEqual(engine, self.client.engine)

        @self.client.engine.on_stop.connect
        def on_stop_receiever(self, engine):
            that.assertEqual(engine, self.client.engine)

        self.client.engine.on_start.send = MagicMock()
        self.client.engine.on_stop.send = MagicMock()
        self.client.start()
        self.client.engine.on_start.send.assert_called_with(self.client.engine)
        raise KeyboardInterrupt
        self.client.engine.on_stop.send.assert_called_with(self.client.engine)
