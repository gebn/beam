# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import os
import sys
import unittest
import mock
import contextlib
from six import StringIO

from beam import __main__


# TODO may actually want to capture stderr so can check error message is correct
# http://stackoverflow.com/a/1810086/2765666
@contextlib.contextmanager
def gobble_stderr():
    saved = sys.stderr

    class DevNull(object):

        def write(self, _):
            pass

        def flush(self):
            pass
    sys.stderr = DevNull()
    try:
        yield
    finally:
        sys.stderr = saved


class TestMain(unittest.TestCase):

    @mock.patch('sys.stderr', new_callable=StringIO)
    def test_print_error(self, mock_stderr):
        error_message = 'this is the error message'
        __main__._print_error(error_message)
        self.assertEqual(mock_stderr.getvalue(), error_message + os.linesep)

    def test_parse_args_none(self):
        with self.assertRaises(SystemExit), gobble_stderr():
            __main__._parse_args([])

    def test_parse_args_host_only(self):
        with self.assertRaises(SystemExit), gobble_stderr():
            __main__._parse_args(['nyc-1'])

    def test_parse_args_no_action(self):
        with self.assertRaises(SystemExit), gobble_stderr():
            __main__._parse_args(['nyc-1', '-A'])

    def test_parse_args_no_attribute(self):
        with self.assertRaises(SystemExit), gobble_stderr():
            __main__._parse_args(['nyc-1', '-a'])

    def test_get_attribute_none_object(self):
        with self.assertRaises(AttributeError):
            __main__._get_attribute(None, 'bar.baz')

    def test_get_attribute_none_attribute(self):
        with self.assertRaises(ValueError):
            __main__._get_attribute('foo', None)
