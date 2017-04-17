#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# GNU GPLv3 <https://www.gnu.org/licenses/gpl-3.0.en.html>

import time
import logging
import unittest
import multiprocessing
from unittest.mock import MagicMock


from neat import const
from neat.scheduler.simple import SimpleDelayScheduler

import blinker


class SimpleDelaySchedulerTest(unittest.TestCase):

    def setUp(self):
        const.log_level = logging.CRITICAL
        self._default_obj = SimpleDelayScheduler()
        self._various_objs = [
            SimpleDelayScheduler(1),
            SimpleDelayScheduler(2),
            SimpleDelayScheduler(3)
        ]

    def tearDown(self):
        del self._default_obj
        for scheduler in self._various_objs:
            del scheduler

    def test_initialization(self):
        self.assertEquals(self._default_obj.delay, 1)
        self.assertIsInstance(self._default_obj.delay, float)
        for scheduler in self._various_objs:
            self.assertIsInstance(scheduler, multiprocessing.Process)
            self.assertIsInstance(scheduler.delay, float)

    def test_run(self):
        signals_recieved = []
        for scheduler in self._various_objs:

            @scheduler.signal.connect
            def signal_receiver(ret_scheduler):
                signals_recieved.append(ret_scheduler)
                that.assertIsInstance(ret_scheduler, SimpleDelayScheduler)
                that.assertEqual(scheduler, ret_scheduler)

            scheduler.signal.send = MagicMock()
            self.assertIsNone(scheduler.run())
            self.assertEqual(True, scheduler.daemon)
        raise KeyboardInterrupt()
