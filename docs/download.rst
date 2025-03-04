Downloading Products
====================

In order to download GLDAS NOAH products you have to register an account with
NASA's Earthdata portal at `<https://disc.gsfc.nasa.gov/>`_.

After that you can use the command line program ``gldas_download`` together with your username and password.

For example to download all GLDAS Noah v2.1 Images (3-hourly) in the period from June 3 to 6 2018
into the local directory `/tmp`, you'd call (with your username and password):

.. code::

   gldas_download /tmp -s 2018-06-03 -e 2018-06-05 --product GLDAS_Noah_v21_025 --username **USERNAME** --password **PASSWORD**

would download GLDAS Noah version 2.1 data from the select start to the selected end day into the '/tmp' folder.

For a description of the download function and all options run

.. code::

    gldas_download -h
