#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# GNU GPLv3 <https://www.gnu.org/licenses/gpl-3.0.en.html>

import logging
import unittest
from unittest.mock import MagicMock

from neat import const
from neat.models.record import Record
from neat.translator import get_translator, ObviusTranslator


class ObviusTranslatorTest(unittest.TestCase):

    def setUp(self):
        const.log_level = logging.CRITICAL
        self._valid_dat = '''<?xml version="1.0" encoding="UTF-8" ?>
        <DAS>
            <name>001EC600070F</name>
            <serial>001EC600070F</serial>
            <devices>
                <device>
                    <name>Broyhill Wind Turbine</name>
                    <address>4</address>
                    <type>Turbine</type>
                    <class>8000</class>
                    <status>Ok</status>
                    <numpoints>16</numpoints>
                    <records>
                        <record>
                            <time zone="UTC">2017-02-24 16:06:22</time>
                            <age units="seconds">59</age>
                            <error text="Ok">0</error>
                            <point number="0" name="Inverter Reactive Power" units="kVAR" value="0.214"  />
                            <point number="1" name="Inverter Real Power" units="kW" value="1.153"  />
                            <point number="2" name="RMS Line Voltage Phase A-N" units="Volts" value="278.874"  />
                            <point number="3" name="RMS Line Voltage Phase B-N" units="Volts" value="279.530"  />
                            <point number="4" name="RMS Line Voltage Phase C-N" units="Volts" value="278.169"  />
                            <point number="5" name="RMS Line Current Phase A" units="Amps" value="2.961"  />
                            <point number="6" name="RMS Line Current Phase B" units="Amps" value="3.130"  />
                            <point number="7" name="RMS Line Current Phase C" units="Amps" value="2.830"  />
                            <point number="8" name="Grid Frequency" units="Hz" value="59.985"  />
                            <point number="9" name="Ambient Temperature" units="Degrees F" value="59.756"  />
                            <point number="10" name="Rotor Speed" units="RPM" value="32.819"  />
                            <point number="11" name="Inverter Energy Total" units="kWh" value="790338.000"  />
                            <point number="12" name="Wind Speed (10 minute average)" units="MPH" value="7.843"  />
                            <point number="13" name="Wind Speed (1 minute average)" units="MPH" value="10.924"  />
                            <point number="14" name="Wind speed (1 second average)" units="MPH" value="10.781"  />
                            <point number="15" name="Turbine Run Time" units="hours" value="49126.903"  />
                        </record>
                    </records>
                </device>
            </devices>
        </DAS>'''
        self._invalid_dat = '''<?xml version="1.0" encoding="UTF-8" ?>
        <DAS>
            <name>001EC600070F</name>
            <serial>001EC600070F</serial>
            <devices>
                <device>
                    <name>Broyhill Wind Turbine</name>
                    <address>4</address>
                    <type>Turbine</type>
                    <class>8000</class>
                    <status>Ok</status>
                    <numpoints>16</numpoints>
                    <records>
                        <record>
                            <time zone="UTC">2017-02-24 16:06:22</time>
                            <age units="seconds">59</age>
                            <error text="Ok">1</error>
                            <point number="0" name="Inverter Reactive Power" units="kVAR" value="0.214"  />
                            <point number="1" name="Inverter Real Power" units="kW" value="1.153"  />
                            <point number="2" name="RMS Line Voltage Phase A-N" units="Volts" value="278.874"  />
                            <point number="3" name="RMS Line Voltage Phase B-N" units="Volts" value="279.530"  />
                            <point number="4" name="RMS Line Voltage Phase C-N" units="Volts" value="278.169"  />
                            <point number="5" name="RMS Line Current Phase A" units="Amps" value="2.961"  />
                            <point number="6" name="RMS Line Current Phase B" units="Amps" value="3.130"  />
                            <point number="7" name="RMS Line Current Phase C" units="Amps" value="2.830"  />
                            <point number="8" name="Grid Frequency" units="Hz" value="59.985"  />
                            <point number="9" name="Ambient Temperature" units="Degrees F" value="59.756"  />
                            <point number="10" name="Rotor Speed" units="RPM" value="32.819"  />
                            <point number="11" name="Inverter Energy Total" units="kWh" value="790338.000"  />
                            <point number="12" name="Wind Speed (10 minute average)" units="MPH" value="7.843"  />
                            <point number="13" name="Wind Speed (1 minute average)" units="MPH" value="10.924"  />
                            <point number="14" name="Wind speed (1 second average)" units="MPH" value="10.781"  />
                            <point number="15" name="Turbine Run Time" units="hours" value="49126.903"  />
                        </record>
                    </records>
                </device>
            </devices>
        </DAS>'''
        self._obj = ObviusTranslator()

    def tearDown(self):
        del self._obj

    def test_initialization(self):
        self.assertIsInstance(self._obj.parser, str)
        self.assertIn(self._obj.parser, self._obj._parser_pref)
        self.assertIsInstance(self._obj.unit_map, dict)

    def test_validate(self):
        self.assertEqual(True, self._obj.validate(self._valid_dat))
        self.assertEqual(False, self._obj.validate(self._invalid_dat))

    def test_translate(self):
        that = self

        @self._obj.signal.connect
        def test_receiver(record: Record):
            that.assertIsInstance(record, Record)

        self._obj.signal.send = MagicMock()
        self.assertIsNone(self._obj.translate(self._valid_dat))
        self.assertEqual(True, self._obj.signal.send.called)
