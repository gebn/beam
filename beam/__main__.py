#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division
import sys
import argparse
import functools

import beam


def _print_error(msg):
    """
    Print a string to stderr.

    :param msg: The message to print.
    """
    print(msg, file=sys.stderr)


def _parse_args():
    parser = argparse.ArgumentParser(prog='beam',
                                     description='A lightweight wrapper for '
                                                 'the SolusVM client API.')
    parser.add_argument('-V', '--version',
                        action='version',
                        version='%(prog)s ' + beam.__version__)
    parser.add_argument('host',
                        help='the identifier of the host whose information to '
                             'retrieve')
    parser.add_argument('attributes',
                        nargs='+',
                        help='one or more attributes of the host to retrieve')
    return parser.parse_args()


def _get_attribute(obj, attribute):
    return functools.reduce(getattr, attribute.split('.'), obj)


def main():
    args = _parse_args()
    try:
        host = beam.host(args.host)
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
    except ValueError:
        _print_error('Host {0} not defined'.format(args.host))
        return 1


if __name__ == '__main__':
    sys.exit(main())
