# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division
import unittest

from beam.resource import Resource


class TestResource(unittest.TestCase):

    _USED_BYTES = 100
    _FREE_BYTES = 50

    @classmethod
    def setUpClass(cls):
        cls.resource = Resource(cls._USED_BYTES, cls._FREE_BYTES)

    def test_used_bytes(self):
        self.assertEqual(self.resource.used_bytes, self._USED_BYTES)

    def test_free_bytes(self):
        self.assertEqual(self.resource.free_bytes, self._FREE_BYTES)

    def test_total_bytes(self):
        self.assertEqual(self.resource.total_bytes,
                         self._USED_BYTES + self._FREE_BYTES)

    def test_used_percentage(self):
        self.assertAlmostEqual(
            self.resource.used_percentage,
            self._USED_BYTES / (self._USED_BYTES + self._FREE_BYTES),
            2)

    def test_free_percentage(self):
        self.assertAlmostEqual(
            self.resource.free_percentage,
            1 - self._USED_BYTES / (self._USED_BYTES + self._FREE_BYTES),
            2)

    def test_percentages_sum_to_one(self):
        resource = Resource(14682693209, 522188218791)
        self.assertEqual(resource.used_percentage + resource.free_percentage,
                         1)

    def test_zero_total_bytes(self):
        self.assertEqual(Resource(0, 0).used_percentage, 1)

    def test_from_response_none(self):
        with self.assertRaises(ValueError):
            Resource.from_response(None)

    def test_from_response_too_many_fragments(self):
        with self.assertRaises(ValueError):
            Resource.from_response('12884901888,6155997184,6728904704,48,22')

    def test_from_response_too_few_fragments(self):
        with self.assertRaises(ValueError):
            Resource.from_response('12884901888,6155997184,6728904704')

    def test_from_response_float(self):
        with self.assertRaises(ValueError):
            Resource.from_response('12884901.888,6155997184,6728904704,48')

    def test_from_response_string(self):
        with self.assertRaises(ValueError):
            Resource.from_response('12884901888,surprise,6728904704,48')

    def test_from_response(self):
        self.assertEqual(Resource(6155997184, 6728904704),
                         Resource.from_response('12884901888,6155997184,'
                                                '6728904704,48'))

    def test_eq_false_class(self):
        self.assertNotEqual(22, self.resource)

    def test_eq_false_used(self):
        self.assertNotEqual(self.resource, Resource(50, 50))

    def test_eq_false_free(self):
        self.assertNotEqual(self.resource, Resource(100, 100))

    def test_eq_true(self):
        self.assertEqual(self.resource, self.resource)

    def test_str(self):
        resource = Resource(6155997184, 6728904704)
        self.assertEqual(str(resource),
                         'Resource(6155997184 bytes used (47.78%), 6728904704 '
                         'bytes free (52.22%))')
