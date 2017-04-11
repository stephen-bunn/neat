#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# GNU GPLv3 <https://www.gnu.org/licenses/gpl-3.0.en.html>

import sys
import inspect

from . import _common
from .obvius import ObviusTranslator


def get_translator(requester_name):
    for (translator_name, translator) in inspect.getmembers(
        sys.modules[__name__], inspect.isclass
    ):
        if requester_name in translator.supported_requesters:
            return translator
