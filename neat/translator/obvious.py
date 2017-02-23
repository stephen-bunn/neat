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
    :created: 02-16-2017 15:16:44
    :modified: 02-16-2017 15:16:44
.. moduleauthor:: Stephen Bunn <r>
"""

import xml.etree.ElementTree
from typing import List

from .. import const
from ._common import AbstractTranslator


class ObviousTranslator(AbstractTranslator):

    @staticmethod
    def translate(data: str) -> dict:
        # TODO: translate content
        print(data)
        # etree = xml.etree.ElementTree.fromstring(data)
        # print(etree)
