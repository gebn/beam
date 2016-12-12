# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import six


@six.python_2_unicode_compatible
class Vendor(object):
    """
    Represents a VPS provider.
    """

    def __init__(self, name, endpoint):
        """
        Initialise a new vendor object.

        :param name: The name of the vendor, e.g. "RamNode".
        :param endpoint: The hostname of the SolusVM control panel, with
                         protocol.
        """
        self.name = name
        self.endpoint = endpoint

    def __hash__(self):
        """
        Retrieve a hash value for this object.

        :return: This object's hash. Identical objects will have an identical
                 hash.
        """
        return hash(self.name)

    def __eq__(self, other):
        """
        Test whether this vendor is identical to another.

        :param other: The object to compare to this one.
        :return: True if the objects are identical, false otherwise.
        """
        return isinstance(other, self.__class__) and other.name == self.name

    def __str__(self):
        """
        Generate a human-readable string representation of this vendor.

        :return: This host as a friendly string.
        """
        return '{0}({1}, {2})'.format(self.__class__.__name__,
                                      self.name,
                                      self.endpoint)
