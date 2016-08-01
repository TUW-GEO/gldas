=====
gldas
=====

.. image:: https://travis-ci.org/TUW-GEO/gldas.svg?branch=master
    :target: https://travis-ci.org/TUW-GEO/gldas

.. image:: https://coveralls.io/repos/github/TUW-GEO/gldas/badge.svg?branch=master
   :target: https://coveralls.io/github/TUW-GEO/gldas?branch=master

.. image:: https://badge.fury.io/py/gldas.svg
    :target: http://badge.fury.io/py/gldas

.. image:: https://zenodo.org/badge/12761/TUW-GEO/gldas.svg
   :target: https://zenodo.org/badge/latestdoi/12761/TUW-GEO/gldas

Readers and converters for data from the `GLDAS Noah Land Surface Model
<http://disc.sci.gsfc.nasa.gov/services/grads-gds/gldas>`_. Written in Python.

Works great in combination with `pytesmo <https://github.com/TUW-GEO/pytesmo>`_.

Downloading products
====================

In order to download GLDAS NOAH products you have to register an account with
NASA's Earthdata portal. Instructions for can be found `here
<http://disc.sci.gsfc.nasa.gov/registration/registration-for-data-access>`_.

After that you can use the command line program ``gldas_download``.

.. code::

   mkdir ~/workspace/gldas_data
   gldas_download ~/workspace/gldas_data

would download GLDAS Noah version 1 in 0.25 degree sampling into the folder
``~/workspace/gldas_data``. For more options run ``gldas_download -h``.

Supported Products
==================

At the moment this package only supports GLDAS Noah data version 1 in grib
format with a spatial sampling of 0.25 degrees. It should be easy to extend the
package to support other GLDAS based products. This will be done as need arises.

Documentation
=============

|Documentation Status|

.. |Documentation Status| image:: https://readthedocs.org/projects/gldas/badge/?version=latest
   :target: http://gldas.readthedocs.org/
