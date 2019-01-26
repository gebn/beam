#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import sys
import argparse
import socket
import functools

import beam
from beam.host import Host


def _print_error(msg):
    """
    Print a string to stderr.

    :param msg: The message to print.
    """
    print(msg, file=sys.stderr)


def _parse_args(argv):
    """
    Interpret argv.

    :param argv: Command line options and positional arguments.
    :return: The namespace resulting from a successful parsing.
    """
    parser = argparse.ArgumentParser(prog='beam',
                                     description='A lightweight wrapper for '
                                                 'the SolusVM client API.')
    parser.add_argument('-V', '--version',
                        action='version',
                        version='%(prog)s ' + beam.__version__)
    parser.add_argument('host',
                        nargs='?', default=socket.gethostname(),
                        help='the identifier of the host whose information to '
                             'retrieve')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-A', '--action',
                       help='an action to execute against the host',
                       choices=Host.VALID_ACTIONS)
    group.add_argument('-a', '--attributes',
                       nargs='+',
                       help='one or more attributes of the host to retrieve')
    return parser.parse_args(argv[1:])


def _get_attribute(obj, attribute):
    """
    Retrieve an attribute denoted by a dotted string from an object.
    e.g. `_get_attribute(foo, 'bar.baz')` = `foo.bar.baz`

    :param obj: The object to query.
    :param attribute: The (possibly nested) attribute to retrieve as a string.
    :return: The attribute's value.
    :raises ValueError: If attribute is empty.
    """

    if not attribute:
        raise ValueError('An attribute must be specified')

    return functools.reduce(getattr, attribute.split('.'), obj)


def main():
    args = _parse_args(sys.argv)
    try:
        host = beam.host(args.host)
    except ValueError:
        _print_error('Host {0} not defined'.format(args.host))
        return 1

    if args.action:
        try:
            host.action(args.action)
        except (ValueError, RuntimeError) as e:
            _print_error('Failed to execute action: {0}'.format(e))
            return 2

    if not args.attributes:
        print(host)
        return 0

    for attribute in args.attributes:
        try:
            print(_get_attribute(host, attribute))
        except AttributeError:
            # invalid; just print a blank line
            print()
    return 0


if __name__ == '__main__':
    sys.exit(main())
