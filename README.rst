beam
====

.. image:: https://img.shields.io/pypi/status/beam.svg
   :target: https://pypi.python.org/pypi/beam
.. image:: https://img.shields.io/pypi/v/beam.svg
   :target: https://pypi.python.org/pypi/beam
.. image:: https://img.shields.io/pypi/pyversions/beam.svg
.. image:: https://travis-ci.org/gebn/beam.svg?branch=master
   :target: https://travis-ci.org/gebn/beam
.. image:: https://coveralls.io/repos/github/gebn/beam/badge.svg?branch=master
   :target: https://coveralls.io/github/gebn/beam?branch=master

A lightweight Python wrapper for the SolusVM client API.

Features
--------

-  Query a host's memory, bandwidth, IP addresses and storage usage.
-  Configurable to work with any SolusVM provider.

Demo
----

.. code:: python

    import beam

    # get a list of hosts using above 90% of their memory
    hosts = [host for host in beam.hosts()
             if host.memory.used_percentage > .9]

    # get a list of hosts with less than 10 GiB of storage left
    hosts = [host for host in beam.hosts()
             if host.storage.free_bytes < 1024 ** 3 * 10]

Setup
-----

1. Run ``pip install beam`` to download the module.
2. Create your ``.beam.ini`` inventory file.

Inventory
~~~~~~~~~

The inventory file holds information about your hosting provider(s) and host(s),
so beam knows how to contact the relevant API endpoints and what credentials to
use. Here's a sample file:

.. code::

   [special:vendors]
   ramnode = https://vpscp.ramnode.com
   fliphost = https://solus.fliphost.net
   default = ramnode

   [nyc-1]
   key = nyc-1_host_key
   hash = nyc-1_host_hash

   [ams-1]
   key = ams-1_host_key
   hash = ams-1_host_hash
   vendor = fliphost

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

Roadmap
-------

-  Implement ``.boot()``, ``.reboot()`` and ``.shutdown()`` for hosts.
-  Generate documentation.

Etymology
---------

Although "solus" means alone, that's a tad depressing. Solus also conjures up
images of the sun for me. The sun *beam*\ s down - and the name was available on
PyPI - so beam it was.
