# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import unittest

from beam.resource import Resource


class TestResource(unittest.TestCase):

    def test_used_bytes(self):
        self.assertEqual(Resource(100, 50).used_bytes, 100)

    def test_free_bytes(self):
        self.assertEqual(Resource(100, 50).free_bytes, 50)

    def test_total_bytes(self):
        self.assertEqual(Resource(100, 50).total_bytes, 150)

    def test_used_percentage(self):
        self.assertAlmostEqual(Resource(100, 50).used_percentage, 0.666, 2)

    def test_free_percentage(self):
        self.assertAlmostEqual(Resource(100, 50).free_percentage, 0.333, 2)

    def test_percentages_sum_to_one(self):
        resource = Resource(14682693209, 522188218791)
        self.assertEqual(resource.used_percentage + resource.free_percentage,
                         1)

    def test_zero_total_bytes(self):
        self.assertEqual(Resource(0, 0).used_percentage, 1)

    def test_str(self):
        resource = Resource(6155997184, 6728904704)
        self.assertEqual(str(resource),
                         'Resource(6155997184 bytes used (47.78%), 6728904704 '
                         'bytes free (52.22%))')
