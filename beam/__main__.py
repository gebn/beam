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
                                     description='A lightweight Python wrapper '
                                                 'for the SolusVM client API.')
    parser.add_argument('-V', '--version',
                        action='version',
                        version='%(prog)s ' + beam.__version__)
    parser.add_argument('host',
                        help='the identifier of the host whose information to '
                             'retrieve')
    parser.add_argument('attribute',
                        nargs='?',
                        help='the attribute of the host to retrieve')
    return parser.parse_args()


def main():
    args = _parse_args()
    try:
        host = beam.host(args.host)
        if not args.attribute:
            print(host)
            return 0

        print(functools.reduce(getattr, args.attribute.split('.'), host))
        return 0
    except ValueError:
        _print_error('Host {0} not defined'.format(args.host))
        return 1
    except AttributeError:
        _print_error('No such attribute {0}'.format(args.attribute))
        return 2


if __name__ == '__main__':
    sys.exit(main())
