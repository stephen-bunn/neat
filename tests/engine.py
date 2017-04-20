#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# GNU GPLv3 <https://www.gnu.org/licenses/gpl-3.0.en.html>

import logging
import unittest
from unittest.mock import MagicMock


from neat import const
from neat.engine import Engine


class EngineTest(unittest.TestCase):

    def setUp(self):
        const.log_level = logging.CRITICAL
        self._blank_engine = Engine({})

    def tearDown(self):
        del self._blank_engine

    def test_initialization(self):
        self.assertEqual(self._blank_engine._register, {})

    def test_signals(self):
        that = self
        self._blank_engine.on_start.send = MagicMock()
        self._blank_engine.on_stop.send = MagicMock()

        @self._blank_engine.on_start.connect
        def start_receiver(self, engine):
            that.assertIsInstance(engine, Engine)

        @self._blank_engine.on_stop.connect
        def stop_receiver(self, engine):
            that.assertIsInstance(engine, Engine)

        self._blank_engine.start()
        self._blank_engine.on_start.send.assert_called_with(self._blank_engine)
        self._blank_engine.stop()
        self._blank_engine.on_stop.send.assert_called_with(self._blank_engine)
