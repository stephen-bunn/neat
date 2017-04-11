#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 Stephen Bunn (stephen@bunn.io)
# GNU GPLv3 <https://www.gnu.org/licenses/gpl-3.0.en.html>

import unittest


class Example(unittest.TestCase):
    """ An example of a simple unittest.TestCase.

    """

    def setUp(self):
        """ Any necessary setup for the testcase on start up.
        """
        pass

    def tearDown(self):
        """ Any necessary destruction for the testcase on exit.
        """
        pass

    def test_something(self):
        """ A test using the built in unittest assertions.
        """

        self.assertEqual(0, 0)
        self.assertEqual(type('test'), type('no test'))
        self.assertNotEqual(0, 1)
        self.assertNotEqual(False, True)
        self.assertTrue(True)
        self.assertTrue(1)
        self.assertFalse(False)
        self.assertFalse(0)
        self.assertIsNone(None)
        self.assertIsNotNone(True)
        self.assertIn(1, range(3))
        self.assertNotIn(-1, range(3))
        self.assertIsInstance('3', str)
        self.assertIsInstance(3, int)
        self.assertNotIsInstance('3', int)
        self.assertNotIsInstance(3, str)
