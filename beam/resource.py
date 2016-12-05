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
