=====
gldas
=====

|ci| |cov| |pip| |doc|

.. |ci| image:: https://github.com/TUW-GEO/gldas/actions/workflows/ci.yml/badge.svg?branch=master
   :target: https://github.com/TUW-GEO/gldas/actions

.. |cov| image:: https://coveralls.io/repos/TUW-GEO/gldas/badge.png?branch=master
  :target: https://coveralls.io/r/TUW-GEO/gldas?branch=master

.. |pip| image:: https://badge.fury.io/py/gldas.svg
    :target: http://badge.fury.io/py/gldas

.. |doc| image:: https://readthedocs.org/projects/gldas/badge/?version=latest
   :target: http://gldas.readthedocs.org/

Readers and converters for data from the `GLDAS Noah Land Surface Model
<http://disc.sci.gsfc.nasa.gov/services/grads-gds/gldas>`_. Written in Python.

Works great in combination with `pytesmo <https://github.com/TUW-GEO/pytesmo>`_.

Citation
========

.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.596427.svg
   :target: https://doi.org/10.5281/zenodo.596427

If you use the software in a publication then please cite it using the Zenodo DOI.
Be aware that this badge links to the latest package version.

Please select your specific version at https://doi.org/10.5281/zenodo.596427 to get the DOI of that version.
You should normally always use the DOI for the specific version of your record in citations.
This is to ensure that other researchers can access the exact research artefact you used for reproducibility.

You can find additional information regarding DOI versioning at http://help.zenodo.org/#versioning

Installation
============

This package can be installed via pip from pypi.org. The minimum required
python version is ``3.9``.

To read grib files on Windows systems, it might be necessary to use conda to
install pygrib first:

.. code::

    conda install pygrib

Afterwards you can install the gldas package and all other dependencies via

.. code::

    pip install gldas

Supported Products
==================

At the moment this package supports GLDAS Noah data version 1 in grib
format (reading, time series creation) and GLDAS Noah data version 2.0 and version 2.1 in netCDF format (download, reading, time series creation) with a spatial sampling of 0.25 degrees.
It should be easy to extend the package to support other GLDAS based products.
This will be done as need arises.

Contribute
==========

We are happy if you want to contribute. Please raise an issue explaining what is missing or if you find a bug. We will also gladly accept pull requests against our master branch for new features or bug fixes.

Development setup
-----------------

For Development we also recommend a ``conda`` environment. You can create one
including test dependencies and debugger by running ``conda create -n gldas python=3.12``, then
``conda env update -f environment.yml`` to install all dependencies. Finally, call
``pip install -e .[testing]``. Now everything should be in place to run tests
and develop new features.

Guidelines
----------

If you want to contribute please follow these steps:

- Fork the gldas repository to your account
- Clone the repository, make sure you use ``git clone --recursive`` to also get the test data repository.
- make a new feature branch from the gldas master branch
- Add your feature
- Please include tests for your contributions in one of the test directories. We use py.test so a simple function called test_my_feature is enough
- submit a pull request to our master branch

Note
====

This project has been set up using PyScaffold 2.5.6. For details and usage
information on PyScaffold see http://pyscaffold.readthedocs.org/.
