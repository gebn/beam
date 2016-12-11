# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import six
# noinspection PyUnresolvedReferences
from six.moves import configparser

from beam.vendor import Vendor
from beam.host import HostIdentity


# noinspection PyClassHasNoInit
class _DictConfigParser(configparser.ConfigParser):
    """
    A simple extension to Python's built in ini parser adding a method to
    retrieve the file as a dictionary.
    """

    def as_dict(self):
        """
        Retrieve the currently loaded configuration as a dictionary.

        :return: The currently loaded configuration as a dictionary.
        """
        d = dict(self._sections)
        for k in d:
            d[k] = dict(self._defaults, **d[k])
            d[k].pop('__name__', None)
        return d


class Config(object):
    """
    Represents beam's configuration file.
    """

    # the name of the config file
    _NAME = '.beam.ini'

    # places to look for the above config file, in order
    _PLACES = ['.', os.path.expanduser('~')]

    @property
    def hosts(self):
        """
        Retrieve all defined hosts.

        :return: The list of all hosts defined in the configuration.
        """
        return self._hosts_by_name.values()

    def __init__(self, hosts):
        """
        Initialise a new configuration instance.

        :param hosts: A list of `HostIdentity`s in the configuration.
        :raises ValueError: If the list of hosts is empty.
        """
        if not hosts:
            raise ValueError('Configuration must contain at least one host for '
                             'beam to be useful')

        self._hosts_by_name = {host.name: host for host in hosts}
        self._hosts_by_key = {host.key: host for host in hosts}
        self._hosts_by_hash = {host.hash: host for host in hosts}

    def find_host(self, identifier):
        """
        Retrieve a host by one of its unique identifiers.

        :param identifier: The host identifier to look up.
        :return: The matching host.
        :raises ValueError: If no such host matches.
        """
        if identifier in self._hosts_by_name:
            return self._hosts_by_name[identifier]

        if identifier in self._hosts_by_key:
            return self._hosts_by_key[identifier]

        if identifier in self._hosts_by_hash:
            return self._hosts_by_hash[identifier]

        raise ValueError('No host found matching {0}'.format(identifier))

    @staticmethod
    def from_ini(path):
        """
        Create a configuration instance from a .ini file.

        :param path: The path to the ini file.
        :return: The parsed configuration.
        :raises ValueError: If parsing fails, or the configuration is malformed.
        """
        parser = _DictConfigParser()
        try:
            # return value is not helpful - check exceptions instead
            parser.read(path)
        except configparser.Error:
            raise ValueError('Failed to parse ini file at {0}'.format(path))
        values = parser.as_dict()

        # create a vendor dictionary with default
        if 'special:vendors' not in values:
            raise ValueError(
                'Config file must contain a special:vendors section')
        vendors = dict(six.iteritems(values.pop('special:vendors')))
        default_vendor = vendors.pop('default', None)  # None must be explicit
        if not vendors:
            raise ValueError('At least one vendor must be defined')

        if not default_vendor:
            # not specified
            if len(vendors) > 1:
                raise ValueError('A default vendor must be specified when more '
                                 'than one is configured')
            # the default vendor is the only vendor
            default_vendor = six.next(six.iterkeys(vendors))
        elif default_vendor not in vendors:
            # specified, but invalid
            raise ValueError('The default vendor specified does not correspond '
                             'to a defined vendor')

        vendors = {name: Vendor(name, endpoint)
                   for name, endpoint in six.iteritems(vendors)}
        default_vendor = vendors[default_vendor]

        # use a normal for loop so we can make exceptions more informative
        hosts = []
        for name, attrs in six.iteritems(values):
            if 'vendor' in attrs:
                if attrs['vendor'] not in vendors:
                    raise ValueError(
                        'Undefined vendor {0} for host {1}'.format(
                            attrs['vendor'], name))
                vendor = vendors[attrs['vendor']]
            else:
                vendor = default_vendor

            if 'key' not in attrs:
                raise ValueError('Host {0} is missing its key'.format(name))
            if 'hash' not in attrs:
                raise ValueError(
                    'Host {0} is missing its hash'.format(name))
            hosts.append(HostIdentity(name,
                                      attrs['key'],
                                      attrs['hash'],
                                      vendor))
        return Config(hosts)

    @classmethod
    def resolve(cls):
        """
        Attempt to find and parse the config file.

        :return: The parsed config file.
        :raises RuntimeError: If the file could not be located.
        """
        for place in cls._PLACES:
            path = os.path.join(place, cls._NAME)
            if os.path.isfile(path):
                return cls.from_ini(path)
        raise RuntimeError('Unable to locate config file')
