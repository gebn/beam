# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import unittest
import responses

from beam.resource import Resource
from beam.host import Host, HostIdentity
from beam.vendor import Vendor


class TestHostIdentity(unittest.TestCase):

    _NAME = 'name'
    _KEY = 'key'
    _HASH = 'hash'
    _VENDOR = Vendor('vendor-name', 'vendor-endpoint')

    @classmethod
    def setUpClass(cls):
        cls.identity = HostIdentity(cls._NAME, cls._KEY, cls._HASH, cls._VENDOR)
        cls.other_identity = HostIdentity(cls._NAME, cls._KEY, 'h', cls._VENDOR)

    def test_request_pams(self):
        self.assertDictEqual(self.identity.request_params,
                             {'key': self._KEY, 'hash': self._HASH})

    def test_hash_match(self):
        self.assertEqual(hash(self.identity), hash(self.identity))

    def test_hash_different(self):
        self.assertNotEqual(hash(self.other_identity), hash(self.identity))

    def test_eq_false_class(self):
        self.assertNotEqual(22, self.identity)

    def test_eq_false_hash(self):
        self.assertNotEqual(self.other_identity, self.identity)

    def test_str(self):
        self.assertEqual(str(self.identity),
                         'HostIdentity({0}, {1})'.format(self._NAME,
                                                         self._VENDOR.name))


class TestHost(unittest.TestCase):
    _VENDOR_ENDPOINT = 'https://vpscp.ramnode.com'
    IDENTITY = HostIdentity('host-name', 'host-key', 'host-hash',
                            Vendor('vendor-name', _VENDOR_ENDPOINT))
    _FQDN = 'host.example.com'
    _PRIMARY_IP = '8.8.8.8'
    _IS_ONLINE = True
    _MEMORY = Resource(100, 100)
    _STORAGE = Resource(200, 200)
    _BANDWIDTH = Resource(300, 300)
    _IP_ADDRESSES = [_PRIMARY_IP, '10.10.10.10']
    _XML = '''<ipaddr>{0}</ipaddr>
<hdd>200,100,100,50</hdd>
<bw>400,200,200,50</bw>
<mem>600,300,300,50</mem>
<status>{1}</status>
<statusmsg></statusmsg>
<hostname>{2}</hostname>
<ipaddress>{3}</ipaddress>
<vmstat>{4}</vmstat>'''
    _XML_VALID = _XML.format(','.join(_IP_ADDRESSES),
                             'success',
                             _FQDN,
                             _PRIMARY_IP,
                             'online' if _IS_ONLINE else 'offline')
    HOST = Host(IDENTITY, _FQDN, _PRIMARY_IP, _IS_ONLINE, _MEMORY, _STORAGE,
                _BANDWIDTH, _IP_ADDRESSES)

    @classmethod
    def setUpClass(cls):
        cls.host = Host(cls.IDENTITY, cls._FQDN, cls._PRIMARY_IP,
                        cls._IS_ONLINE, cls._MEMORY, cls._STORAGE,
                        cls._BANDWIDTH, cls._IP_ADDRESSES)

    @staticmethod
    def _make_host(identity=IDENTITY, fqdn=_FQDN, primary_ip=_PRIMARY_IP,
                   is_online=_IS_ONLINE, memory=_MEMORY, storage=_STORAGE,
                   bandwidth=_BANDWIDTH, ip_addresses=_IP_ADDRESSES):
        return Host(identity, fqdn, primary_ip, is_online, memory, storage,
                    bandwidth, ip_addresses)

    @staticmethod
    def add_response(verb=responses.GET,
                     url=_VENDOR_ENDPOINT + '/api/client/command.php',
                     body=_XML_VALID,
                     status=200):
        responses.add(verb, url, body, status=status)

    @responses.activate
    def test_request_from_identity_denied(self):
        self.add_response(status=403)
        with self.assertRaises(RuntimeError):
            Host.request_from_identity(self.IDENTITY)

    @responses.activate
    def test_request_from_identity(self):
        responses.add(
            responses.GET,
            self._VENDOR_ENDPOINT + '/api/client/command.php',
            status=200,
            body=self._XML_VALID)
        self.assertEqual(Host.request_from_identity(self.IDENTITY),
                         self.host)

    def test_is_offline_false(self):
        self.assertFalse(self.host.is_offline)

    def test_is_offline_true(self):
        self.assertTrue(self._make_host(is_online=False).is_offline)

    def test_from_response_none(self):
        with self.assertRaises(ValueError):
            Host.from_response(None, self.IDENTITY)

    def test_from_response_malformed(self):
        with self.assertRaises(ValueError):
            Host.from_response('><', self.IDENTITY)

    def test_from_response_api_failure(self):
        with self.assertRaises(RuntimeError):
            Host.from_response(self._XML.format(','.join(self._IP_ADDRESSES),
                                                'failure',
                                                self._FQDN,
                                                self._PRIMARY_IP,
                                                'online' if self._IS_ONLINE
                                                else 'offline'),
                               self.IDENTITY)

    def test_from_response_missing_attribute(self):
        with self.assertRaises(ValueError):
            Host.from_response('<root/>', self.IDENTITY)

    def test_from_response(self):
        self.assertEqual(
            Host.from_response(self._XML_VALID, self.IDENTITY),
            self.host)

    def test_str(self):
        self.assertEqual(str(self.host),
                         '{0}({1})'.format(Host.__name__, self._FQDN))
