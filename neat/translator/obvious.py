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

from typing import List

from .. import const
from ._common import AbstractTranslator
from ..requester.obvious import ObviousRequester

import blinker


class ObviousTranslator(AbstractTranslator):

    def __init__(self, requesters: List[ObviousRequester]):
        self.requesters = requesters

    @property
    def requesters(self) -> List[ObviousRequester]:
        return self._requesters

    @requesters.setter
    def requesters(self, requesters: List[ObviousRequester]):
        self._requesters = requesters
        for r in self._requesters:
            r.signal.connect(self.translate)

    def translate(self, requester: ObviousRequester, data: str) -> dict:
        # TODO: translate content
        const.log.debug((
            'received signal from `{requester.signal_name}` ...'
        ).format(requester=requester))
        print(requester, data)
