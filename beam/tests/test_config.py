# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import unittest
import os
import six
try:
    from unittest import mock
except ImportError:
    import mock

# noinspection PyProtectedMember
from beam.config import Config, _DictConfigParser as DictConfigParser
from beam.host import HostIdentity
from beam.vendor import Vendor


def _config_path(name):
    return os.path.join(os.path.dirname(__file__), 'configs', name)


# valid examples
_VALID_INI = _config_path('valid.ini')
_IMPLICIT_DEFAULT_VENDOR_INI = _config_path('implicit_default_vendor.ini')
_EXPLICIT_VENDOR_INI = _config_path('explicit_vendor.ini')

# invalid examples
_EMPTY_INI = _config_path('empty.ini')
_MALFORMED_INI = _config_path('malformed.ini')
_MISSING_VENDORS_INI = _config_path('missing_vendors.ini')
_EMPTY_VENDORS_INI = _config_path('empty_vendors.ini')
_DEFAULT_VENDOR_INVALID_INI = _config_path('default_vendor_invalid.ini')
_DEFAULT_VENDOR_UNDEFINED_INI = _config_path('default_vendor_undefined.ini')
_DEFAULT_VENDOR_UNSPECIFIED_INI = _config_path('default_vendor_unspecified.ini')
_MISSING_HOSTS_INI = _config_path('missing_hosts.ini')
_MISSING_HOST_KEY_INI = _config_path('missing_host_key.ini')
_MISSING_HOST_HASH_INI = _config_path('missing_host_hash.ini')
_HOST_VENDOR_UNDEFINED_INI = _config_path('host_vendor_undefined.ini')


class TestDictConfigParser(unittest.TestCase):
    _VALID_DICT = {
        'special:vendors': {
            'ramnode': 'https://vpscp.ramnode.com',
            'fliphost': 'https://solus.fliphost.net',
            'inception_eu': 'https://vpsadmin.inceptionhosting.com',
            'inception_us': 'https://usadmin.inceptionhosting.com',
            'default': 'ramnode'
        },
        'nyc-1': {
            'key': 'nyc-1_key',
            'hash': 'nyc-1_hash'
        },
        'ams-1': {
            'key': 'ams-1_key',
            'hash': 'ams-1_hash',
            'vendor': 'inception_eu'
        }
    }

    def test_as_dict(self):
        config = DictConfigParser()
        self.assertListEqual([_VALID_INI],
                             config.read(_VALID_INI))
        self.assertDictEqual(config.as_dict(), self._VALID_DICT)


class TestConfig(unittest.TestCase):

    _HOST_A_NAME = 'a'
    _HOST_A_KEY = 'a_key'
    _HOST_A_HASH = 'a_hash'
    _HOST_A_VENDOR = Vendor('a_vendor_name', 'a_vendor_endpoint')
    _HOST_A = HostIdentity(_HOST_A_NAME, _HOST_A_KEY, _HOST_A_HASH,
                           _HOST_A_VENDOR)

    _HOST_B_NAME = 'b'
    _HOST_B_KEY = 'b_key'
    _HOST_B_HASH = 'b_hash'
    _HOST_B_VENDOR = Vendor('b_vendor_name', 'b_vendor_endpoint')
    _HOST_B = HostIdentity(_HOST_B_NAME, _HOST_B_KEY, _HOST_B_HASH,
                           _HOST_B_VENDOR)

    _HOSTS = [_HOST_A, _HOST_B]

    @classmethod
    def setUpClass(cls):
        cls.config = Config(cls._HOSTS)

    def test_init_none(self):
        with self.assertRaises(ValueError):
            Config(None)

    def test_init_empty(self):
        with self.assertRaises(ValueError):
            Config([])

    def test_hosts(self):
        six.assertCountEqual(self, self.config.hosts, self._HOSTS)

    def test_find_host_name(self):
        self.assertEqual(self.config.find_host(self._HOST_B_NAME), self._HOST_B)

    def test_find_host_key(self):
        self.assertEqual(self.config.find_host(self._HOST_B_KEY), self._HOST_B)

    def test_find_host_hash(self):
        self.assertEqual(self.config.find_host(self._HOST_B_HASH), self._HOST_B)

    def test_find_host_fail(self):
        with self.assertRaises(ValueError):
            self.config.find_host('unknown')

    def test_from_ini_empty(self):
        with self.assertRaises(ValueError):
            Config.from_ini(_EMPTY_INI)

    def test_from_ini_malformed(self):
        # must be compatible with 2 and 3 - malformed ini treated differently
        with self.assertRaises(ValueError):
            Config.from_ini(_MALFORMED_INI)

    def test_from_ini_missing_vendors(self):
        with six.assertRaisesRegex(self, ValueError, 'special:vendors section'):
            Config.from_ini(_MISSING_VENDORS_INI)

    def test_from_ini_empty_vendors(self):
        with six.assertRaisesRegex(self, ValueError, 'At least one'):
            Config.from_ini(_EMPTY_VENDORS_INI)

    def test_from_ini_default_vendor_invalid(self):
        with six.assertRaisesRegex(self, ValueError,
                                   'specified does not correspond'):
            Config.from_ini(_DEFAULT_VENDOR_INVALID_INI)

    def test_from_ini_default_vendor_undefined(self):
        with six.assertRaisesRegex(self, ValueError, 'At least one'):
            Config.from_ini(_DEFAULT_VENDOR_UNDEFINED_INI)

    def test_from_ini_default_vendor_unspecified(self):
        with six.assertRaisesRegex(self, ValueError, 'when more than one is'):
            Config.from_ini(_DEFAULT_VENDOR_UNSPECIFIED_INI)

    def test_from_ini_missing_hosts(self):
        with six.assertRaisesRegex(self, ValueError, 'at least one'):
            Config.from_ini(_MISSING_HOSTS_INI)

    def test_from_ini_missing_host_key(self):
        with six.assertRaisesRegex(self, ValueError, 'key'):
            Config.from_ini(_MISSING_HOST_KEY_INI)

    def test_from_ini_missing_host_hash(self):
        with six.assertRaisesRegex(self, ValueError, 'hash'):
            Config.from_ini(_MISSING_HOST_HASH_INI)

    def test_from_ini_host_vendor_undefined(self):
        with six.assertRaisesRegex(self, ValueError,
                                   'Undefined vendor .+ for host'):
            Config.from_ini(_HOST_VENDOR_UNDEFINED_INI)

    def test_from_ini_explicit_vendor(self):
        config = Config.from_ini(_EXPLICIT_VENDOR_INI)
        self.assertEqual(
            config.find_host(self._HOST_A_NAME).vendor,
            self._HOST_B_VENDOR)

    # @unittest.skip('Not implemented')
    # def test_resolve_in_pwd(self, mock_os, mock_path):
    #     # TODO implement
    #     pass
    #
    # @unittest.skip('Not implemented')
    # def test_resolve_in_home(self):
    #     # TODO implement
    #     pass

    @mock.patch('beam.config.os.path')
    def test_resolve_fail(self, mock_path):
        mock_path.isfile.return_value = False
        with self.assertRaises(RuntimeError):
            Config.resolve()
