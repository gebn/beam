# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division

import six
import requests
from xml.etree import cElementTree
from xml.etree.cElementTree import ParseError

from beam.resource import Resource


@six.python_2_unicode_compatible
class HostIdentity(object):
    """
    Represents identification information for a host.
    """

    @property
    def request_params(self):
        """
        Retrieve parameters that identify this host, suitable for inclusion in
        an API request.

        :return: The host parameters dictionary.
        """
        return {'key': self.key, 'hash': self.hash}

    def __init__(self, name, key, hash_, vendor):
        """
        Initialise a new host identity object.

        :param name: The friendly name of the node.
        :param key: The node's key.
        :param hash_: The node's hash.
        :param vendor: The vendor providing this host.
        """
        self.name = name
        self.key = key
        self.hash = hash_
        self.vendor = vendor

    def __hash__(self):
        """
        Retrieve a hash value for this object.

        :return: This object's hash. Identical objects will have an identical
                 hash.
        """
        return hash(self.hash)

    def __eq__(self, other):
        """
        Test whether this host is identical to another.

        :param other: The object to compare to this one.
        :return: True if the objects are identical, false otherwise.
        """
        # could use key xor hash here
        return isinstance(other, self.__class__) and \
            other.hash == self.hash

    def __str__(self):
        """
        Generate a human-readable string representation of this host.

        :return: This host as a friendly string.
        """
        return '{0}({1}, {2})'.format(self.__class__.__name__,
                                      self.name,
                                      self.vendor.name)


@six.python_2_unicode_compatible
class Host(HostIdentity):
    """
    Represents a host with all its metadata.
    """

    # the relative path to the metadata service
    _ENDPOINT = '/api/client/command.php'

    # actions that can be carried out against a host
    VALID_ACTIONS = ['boot', 'reboot', 'shutdown']

    @property
    def is_offline(self):
        """
        Find whether this host is offline.

        :return: True if it is offline, false if it is online.
        """
        return not self.is_online

    def __init__(self, identity, fqdn, primary_ip, is_online, memory, storage,
                 bandwidth, ip_addresses):
        """
        Initialise a new host object.

        :param identity: This host's identity.
        :param fqdn: The node's fully-qualified domain name (sans trailing .).
        :param primary_ip: The node's primary IP(v4/v6) address.
        :param is_online: Whether the node is up.
        :param memory: The state of the node's memory.
        :param storage: The state of the node's storage.
        :param bandwidth: Bandwidth used and remaining.
        :param ip_addresses: All IP addresses assigned to the node.
        """
        super(Host, self).__init__(identity.name, identity.key, identity.hash,
                                   identity.vendor)
        self.fqdn = fqdn
        self.primary_ip = primary_ip
        self.is_online = is_online
        self.memory = memory
        self.storage = storage
        self.bandwidth = bandwidth
        self.ip_addresses = ip_addresses

    def action(self, action):
        """
        Execute an action against this host by name. If always executing the
        same action, use `.boot()`, `.reboot()` or `.shutdown()` instead.

        :param action: The name of the action, e.g. 'reboot'.
        :raises ValueError: If an invalid action is passed.
        :raises RuntimeError: If the SolusVM API indicates failure.
        """

        if action not in self.VALID_ACTIONS:
            raise ValueError('Invalid action: {0}'.format(action))

        data = self.identity.request_params
        data.update({
            'action': action,
            'status': 'true'
        })

        response = requests.post(
            self.identity.vendor.endpoint + self._ENDPOINT, data=data)
        if response.status_code != requests.codes.ok or \
                '<status>success</status>' not in response.text:
            raise RuntimeError(
                'Unable to {0} host: {1}'.format(action, response.text))

    def boot(self):
        """
        Start this host.
        """
        self.action('boot')

    def reboot(self):
        """
        Restart this host.
        """
        self.action('reboot')

    def shutdown(self):
        """
        Turn off this host.
        """
        self.action('shutdown')

    @classmethod
    def request_from_identity(cls, identity):
        """
        Retrieve information about a host.

        :param identity: The host's identification details.
        :return: The retrieved host object.
        :raises RuntimeError: If the API request fails.
        """
        params = identity.request_params
        params.update({
            'action': 'info',
            'ipaddr': 'true',
            'hdd': 'true',
            'mem': 'true',
            'bw': 'true',
            'status': 'true'
        })

        response = requests.get(
            identity.vendor.endpoint + cls._ENDPOINT, params=params)
        if response.status_code != requests.codes.ok:
            raise RuntimeError(
                'Unable to retrieve host: {0}'.format(response.text))
        return cls.from_response(response.text, identity)

    @classmethod
    def from_response(cls, body, identity):
        """
        Create a host object from an API response.

        :param body: The raw API response text.
        :param identity: This host's identity.
        :return: An object representing the host.
        :raises ValueError: If the response is empty or malformed.
        :raises RuntimeError: If the response indicates the API request failed.
        """
        if not body:
            raise ValueError('Cannot construct host from empty response')

        try:
            root = cElementTree.fromstring('<root>' + body + '</root>')

            if root.find('status').text != 'success':
                message = root.find('statusmsg')
                raise RuntimeError(
                    'Response indicates failed API call: {0}'.format(
                        message.text if message else 'unspecified error'))

            return Host(identity,
                        root.find('hostname').text,
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

    def __str__(self):
        """
        Generate a human-readable string representation of this host.

        :return: This host as a friendly string.
        """
        return '{0}({1})'.format(self.__class__.__name__, self.fqdn)
