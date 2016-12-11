# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division
import unittest

from beam.vendor import Vendor


class TestVendor(unittest.TestCase):

    _NAME = 'ramnode'
    _ENDPOINT = 'https://vpscp.ramnode.com'

    @classmethod
    def setUpClass(cls):
        cls.vendor = Vendor(cls._NAME, cls._ENDPOINT)
        cls.other_vendor = Vendor('n', 'e')

    def test_hash_match(self):
        self.assertEqual(hash(self.vendor), hash(self.vendor))

    def test_hash_different(self):
        self.assertNotEqual(hash(self.other_vendor), hash(self.vendor))

    def test_eq_false_class(self):
        self.assertNotEqual(22, self.vendor)

    def test_eq_false_name(self):
        self.assertNotEqual(Vendor('inception', self._ENDPOINT),
                            self.vendor)

    def test_eq_true(self):
        self.assertEqual(self.vendor, self.vendor)

    def test_str(self):
        self.assertEqual(str(self.vendor),
                         'Vendor(ramnode, https://vpscp.ramnode.com)')
