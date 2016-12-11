# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from os import path
import codecs

from beam.config import Config
from beam.host import Host


def _read_file(name, encoding='utf-8'):
    """
    Read the contents of a file.

    :param name: The name of the file in the current directory.
    :param encoding: The encoding of the file; defaults to utf-8.
    :return: The contents of the file.
    """
    with codecs.open(name, encoding=encoding) as f:
        return f.read()


__version__ = _read_file(path.join(path.dirname(__file__), 'VERSION')).strip()

_config = Config.resolve()


def host(identifier):
    """
    Retrieve information about a host.

    :param identifier: The host's name, key or hash.
    :return: The matching host.
    """
    identity = _config.find_host(identifier)
    return Host.request_from_identity(identity)


def hosts():
    """
    Retrieve information about all hosts.
    N.B. This operation can take some time!

    :return: Metadata about every host in the inventory.
    """
    return [host(host_.hash) for host_ in _config.hosts]
