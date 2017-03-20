#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 NEAT Team
# GNU GPLv3 <https://www.gnu.org/licenses/gpl-3.0.en.html>

"""
__init__.py
.. module:: neat
    :platform: Linux, MacOSX, Win32
    :synopsis:
    :created: 01-28-2017 12:53:57
    :modified: 01-28-2017 13:04:03
.. moduleauthor:: NEAT Team
"""

from . import const
from .client import Client
from .engine import Engine
from . import (
    device,
    scheduler,
    requester,
    translator,
    pipe,
)
