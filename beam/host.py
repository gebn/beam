# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division

import six
from xml.etree import cElementTree
from xml.etree.cElementTree import ParseError

from beam.resource import Resource


@six.python_2_unicode_compatible
class Host(object):

    @property
    def is_offline(self):
        """
        Find whether this host is offline.

        :return: True if it is offline, false if it is online.
        """
        return not self.is_online

    def __init__(self, name, key, hash_, fqdn, primary_ip, is_online,
                 memory, storage, bandwidth, ip_addresses):
        """
        Initialise a new host object.

        :param name: The friendly name of the node.
        :param key: The node's key.
        :param hash_: The node's hash.
        :param fqdn: The node's fully-qualified domain name (sans trailing .).
        :param primary_ip: The node's primary IP(v4/v6) address.
        :param is_online: Whether the node is up.
        :param memory: The state of the node's memory.
        :param storage: The state of the node's storage.
        :param bandwidth: Bandwidth used and remaining.
        :param ip_addresses: All IP addresses assigned to the node.
        """
        self.name = name
        self.key = key
        self.hash = hash_
        self.fqdn = fqdn
        self.primary_ip = primary_ip
        self.is_online = is_online
        self.memory = memory
        self.storage = storage
        self.bandwidth = bandwidth
        self.ip_addresses = ip_addresses

    @classmethod
    def from_response(cls, response, name, key, hash_):
        """
        Create a host object from an API response.

        :param response: The raw API response text.
        :param name: The host's alias.
        :param key: The host's key.
        :param hash_: The host's hash.
        :return: An object representing the host.
        :raises ValueError: If the response is empty or malformed.
        :raises RuntimeError: If the response indicates the API request failed.
        """
        if not response:
            raise ValueError('Cannot construct host from empty response')

        try:
            root = cElementTree.fromstring('<root>' + response + '</root>')

            if root.find('status').text != 'success':
                message = root.find('statusmsg')
                raise RuntimeError(
                    'Response indicates failed API call: {0}'.format(
                        message.text if message else 'unspecified error'))

            return Host(name, key, hash_, root.find('hostname').text,
                        root.find('ipaddress').text,
                        root.find('vmstat').text == 'online',
                        Resource.from_response(root.find('mem').text),
                        Resource.from_response(root.find('hdd').text),
                        Resource.from_response(root.find('bw').text),
                        root.find('ipaddr').text.split(','))
        except ParseError as e:
            raise ValueError('Host response is malformed: {0}'.format(e))
        except AttributeError as e:
            raise ValueError(
                'Host response is missing an attribute: {0}'.format(e))

    def __eq__(self, other):
        """
        Test whether this host is identical to another.

        :param other: The object to compare to this one.
        :return: True if the objects are identical, false otherwise.
        """
        # could use key xor hash here
        return isinstance(other, self.__class__) and \
            other.key == self.key and \
            other.hash == self.hash

    def __str__(self):
        """
        Generate a human-readable string representation of this host.

        :return: This host as a friendly string.
        """
        return '{0}({1})'.format(self.__class__.__name__, self.fqdn)
