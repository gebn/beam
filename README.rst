beam
====

.. image:: https://img.shields.io/pypi/status/beam.svg
   :target: https://pypi.python.org/pypi/beam
.. image:: https://img.shields.io/pypi/v/beam.svg
   :target: https://pypi.python.org/pypi/beam
.. image:: https://img.shields.io/pypi/pyversions/beam.svg
   :target: https://pypi.python.org/pypi/beam
.. image:: https://travis-ci.org/gebn/beam.svg?branch=master
   :target: https://travis-ci.org/gebn/beam
.. image:: https://coveralls.io/repos/github/gebn/beam/badge.svg?branch=master
   :target: https://coveralls.io/github/gebn/beam?branch=master

A lightweight wrapper for the SolusVM client API.

Features
--------

-  Query a host's memory, bandwidth, IP addresses and storage usage.
-  Boot, reboot and shutdown machines.
-  Configurable to work with any SolusVM provider.
-  Command line client and intuitive Python module for your own scripts.

Setup
-----

1. Run ``pip install beam`` to download the module.
2. Create your ``.beam.ini`` inventory file as below.

Inventory
~~~~~~~~~

The inventory file holds information about your hosting provider(s) and host(s),
so beam knows how to contact the relevant API endpoints and what credentials to
use. Here's a sample file:

.. code::

   [special:vendors]
   ramnode = https://vpscp.ramnode.com
   vendor2 = https://vendor2-panel.com
   default = ramnode

   [nyc-1]
   key = nyc-1_host_key
   hash = nyc-1_host_hash

   [ams-1]
   key = ams-1_host_key
   hash = ams-1_host_hash
   vendor = vendor2

This file defines two hosts, ``nyc-1``, hosted with RamNode, and ``ams-1``,
hosted with FlipHost. At the top are the vendor names in a special vendors
section (all other sections are assumed to represent hosts). The format maps a
vendor name to their base endpoint for the SolusVM API. The ``default``
directive indicates the implicit vendor of every host, and must be specified if
more than one vendor is defined.

Each host has its own section. The correct ``key`` and ``hash`` values can be
optained from the SolusVM control panel used by your vendor. If a host is not
provided by the default vendor, a ``vendor`` directive specifies the correct
one.

Usage
-----

Beam provides both a Python library for programmatic access to your hosts, and
a simple CLI that wraps it in a couple of lines of code.

CLI
~~~

The CLI client can be used to find information about a single host.

.. code::

    $ beam --help
    usage: beam [-h] [-V]
                (-A {boot,reboot,shutdown} | -a ATTRIBUTES [ATTRIBUTES ...])
                [host]

    A lightweight wrapper for the SolusVM client API.

    positional arguments:
      host                  the identifier of the host whose information to
                            retrieve

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit
      -A {boot,reboot,shutdown}, --action {boot,reboot,shutdown}
                            an action to execute against the host
      -a ATTRIBUTES [ATTRIBUTES ...], --attributes ATTRIBUTES [ATTRIBUTES ...]
                            one or more attributes of the host to retrieve
    $ beam -a bandwidth.free_percentage nyc-1
    0.4983459835
    $ beam -a primary_ip lon-1
    2604:180:2:32b::498b
    $ beam -a is_online memory.used_bytes ams-1
    True
    34578234983
    $ beam -A shutdown nyc-1
    OK

Library
~~~~~~~

.. code:: python

    import beam

    # shutdown a specific host
    host = beam.host('nyc-1')  # name, key or hash
    if host.is_online:
        host.shutdown()

    # boot all offline hosts
    [host.boot() for host in beam.hosts() if not host.is_online]

    # get a list of hosts using above 90% of their memory
    hosts = [host for host in beam.hosts()
             if host.memory.used_percentage > .9]

    # get a list of hosts with less than 10 GiB of storage left
    hosts = [host for host in beam.hosts()
             if host.storage.free_bytes < 1024 ** 3 * 10]

Roadmap
-------

-  Generate documentation.
-  Increase unit test coverage to 100%, and implement some integration tests.

Etymology
---------

Although "solus" means alone, that's a tad depressing. Solus also conjures up
images of the sun for me. The sun *beam*\ s down - and the name was available on
PyPI - so beam it was.
