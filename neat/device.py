#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn <r>
# GNU GPLv3 <https://www.gnu.org/licenses/gpl-3.0.en.html>

"""
device.py
    :platform: Linux, MacOSX, Win32
    :synopsis:
    :created: 03-13-2017 19:18:22
    :modified: 03-13-2017 19:18:22
.. moduleauthor:: Stephen Bunn <r>
"""

import enum


class DeviceType(enum.Enum):
    """ An enumeration of available device types.
    """

    UNKNOWN = ('UNKNOWN', 0x0)
    PV = ('PV', 0x1)
    HVAC = ('HVAC', 0x2)
    SOLAR_THERM = ('SOLAR_THERM', 0x3)
    WIND = ('WIND', 0x4)
    FLOW = ('FLOW', 0x5)
    ENERGY = ('ENERGY', 0x6)
    TEMP = ('TEMP', 0x7)
