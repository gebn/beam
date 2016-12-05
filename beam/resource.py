# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division

import six


@six.python_2_unicode_compatible
class Resource(object):
    """
    Represents the state of any server resource measured in bytes with the
    concept of scarcity.
    """

    def __init__(self, used_bytes, free_bytes):
        """
        Initialise a new resource instance. If the total number of bytes is 0,
        100% usage will be indicated for safety.

        :param used_bytes: The number of bytes of this resource used.
        :param free_bytes: The remaining number of bytes that can be used.
        """
        self.used_bytes = used_bytes
        self.free_bytes = free_bytes
        self.total_bytes = used_bytes + free_bytes
        self.used_percentage = 1 if not self.total_bytes else \
            used_bytes / self.total_bytes
        self.free_percentage = 1 - self.used_percentage

    @staticmethod
    def from_response(response):
        """
        Parse a comma-separated string returned by SolusVM's API into a
        resource object.

        :param response: The value string to parse.
        :return: A resource object representing the same string.
        :raises ValueError: If the value is malformed.
        """

        if not response:
            raise ValueError('Cannot construct resource from empty response')

        try:
            fragments = [int(chunk) for chunk in response.split(',')]
            if len(fragments) != 4:
                raise ValueError('Incorrect number of fragments in response')
            return Resource(fragments[1], fragments[2])
        except ValueError:
            raise ValueError('Invalid byte count in response')

    def __eq__(self, other):
        """
        Test whether this resource is identical to another.

        :param other: The object to compare to this one.
        :return: True if the objects are identical, false otherwise.
        """
        return isinstance(other, self.__class__) and \
            other.used_bytes == self.used_bytes and \
            other.free_bytes == self.free_bytes

    def __str__(self):
        """
        Generate a human-readable string representation of this resource's
        state.

        :return: This resource as a friendly string.
        """
        return '{0}({1} bytes used ({2:.2%}), {3} bytes free ({4:.2%}))'.format(
            self.__class__.__name__,
            self.used_bytes,
            self.used_percentage,
            self.free_bytes,
            self.free_percentage)
