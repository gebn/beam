# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import unittest

from beam.resource import Resource
from beam.host import Host


class TestHost(unittest.TestCase):
    
    _NAME = 'this-is-the-name'
    _KEY = 'this-is-the-key'
    _HASH = 'this-is-the-hash'
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
    
    @classmethod
    def setUpClass(cls):
        cls.host = Host(cls._NAME, cls._KEY, cls._HASH, cls._FQDN,
                        cls._PRIMARY_IP, cls._IS_ONLINE, cls._MEMORY,
                        cls._STORAGE, cls._BANDWIDTH, cls._IP_ADDRESSES)

    @staticmethod
    def _make_host(name=_NAME, key=_KEY, hash_=_HASH, fqdn=_FQDN,
                   primary_ip=_PRIMARY_IP, is_online=_IS_ONLINE, memory=_MEMORY,
                   storage=_STORAGE, bandwidth=_BANDWIDTH,
                   ip_addresses=_IP_ADDRESSES):
        return Host(name, key, hash_, fqdn, primary_ip, is_online, memory,
                    storage, bandwidth, ip_addresses)

    def test_is_offline_false(self):
        self.assertFalse(self.host.is_offline)
    
    def test_is_offline_true(self):
        self.assertTrue(self._make_host(is_online=False).is_offline)

    def test_from_response_none(self):
        with self.assertRaises(ValueError):
            Host.from_response(None, self._NAME, self._KEY, self._HASH)

    def test_from_response_malformed(self):
        with self.assertRaises(ValueError):
            Host.from_response('bad_xml_here', self._NAME, self._KEY,
                               self._HASH)

    def test_from_response_api_failure(self):
        with self.assertRaises(RuntimeError):
            Host.from_response(self._XML.format(','.join(self._IP_ADDRESSES),
                               'failure',
                               self._FQDN,
                               self._PRIMARY_IP,
                               'online' if self._IS_ONLINE else 'offline'),
                               self._NAME,
                               self._KEY,
                               self._HASH)

    def test_from_response_missing_attribute(self):
        with self.assertRaises(ValueError):
            Host.from_response('<root/>', self._NAME, self._KEY,
                               self._HASH)

    def test_from_response(self):
        self.assertEqual(
            Host.from_response(self._XML.format(','.join(self._IP_ADDRESSES),
                               'success',
                               self._FQDN,
                               self._PRIMARY_IP,
                               'online' if self._IS_ONLINE else 'offline'),
                               self._NAME,
                               self._KEY,
                               self._HASH),
            self.host)

    def test_eq_false_class(self):
        self.assertNotEqual(22, self.host)

    def test_eq_false_key(self):
        self.assertNotEqual(self._make_host(hash_=self._KEY + 'changed'),
                            self.host)

    def test_eq_false_hash(self):
        self.assertNotEqual(self._make_host(hash_=self._HASH + 'changed'),
                            self.host)

    def test_eq_true(self):
        self.assertEqual(self.host, self.host)

    def test_str(self):
        self.assertEqual(str(self.host),
                         '{0}({1})'.format(Host.__name__, self._FQDN))
