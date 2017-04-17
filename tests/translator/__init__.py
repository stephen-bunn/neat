#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# GNU GPLv3 <https://www.gnu.org/licenses/gpl-3.0.en.html>

import unittest

from .obvius import *
from neat.translator import get_translator
from neat.translator._common import AbstractTranslator
from neat.translator.obvius import ObviusTranslator


class get_translatorTest(unittest.TestCase):

    def test_get_translator(self):
        self.assertIsNone(get_translator(''))
        self.assertIsInstance(
            get_translator('ObviusRequester'), AbstractTranslator
        )
        self.assertIsInstance(
            get_translator('ObviusRequester'), ObviusTranslator
        )
