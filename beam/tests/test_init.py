# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division
import unittest
import responses

import beam
from beam.tests.test_host import TestHost


class TestInit(unittest.TestCase):

    @responses.activate
    def test_host(self):
        TestHost.add_response()
        self.assertEqual(beam.host(TestHost.IDENTITY.name),
                         TestHost.HOST)

    @responses.activate
    def test_hosts(self):
        TestHost.add_response()
        self.assertEqual(beam.hosts(), [TestHost.HOST])
