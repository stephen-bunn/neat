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

import importlib

from .. import const
from ._common import AbstractTranslator

import bs4
import pint
import dateutil.parser


class ObviousTranslator(AbstractTranslator):
    _parser_pref = ['lxml', 'html.parser']

    def __init__(self, **kwargs: dict) -> None:
        self._meta = kwargs
        self._unit_reg = pint.UnitRegistry()
        self._unit_map = {

        }

    @property
    def parser(self) -> str:
        if not hasattr(self, '_parser') or \
                self._parser not in self._parser_pref:
            for parser in self._parser_pref:
                if importlib.util.find_spec(parser):
                    self._parser = parser
                    break
        return self._parser

    @property
    def unit_map(self) -> dict:
        pass

    def translate(self, data: str) -> dict:
        soup = bs4.BeautifulSoup(data, self.parser)
        for device in soup.find_all('devices'):
            name = device.find('name').text
            for record in device.find_all('record'):
                rec_timestamp = dateutil.parser.parse(record.find('time').text)
                rec_error = record.find('error').text
                for point in record.find_all('point'):
                    print(point.attrs)
