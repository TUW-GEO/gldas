Reading GLDAS images
--------------------

Reading of the GLDAS raw grib files can be done in two ways.

Reading by file name
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import os
    from datetime import datetime
    from gldas.interface import GLDAS_Noah_v1_025Img

    # read several parameters
    parameter = ['086_L2', '086_L1', '085_L1', '138', '132', '051']
    # the class is initialized with the exact filename.
    img = GLDAS_Noah_v1_025Img(os.path.join(os.path.dirname(__file__),
                                            'test-data',
                                            'GLDAS_NOAH_image_data',
                                            '2015',
                                            '001',
                                            'GLDAS_NOAH025SUBP_3H.A2015001.0000.001.2015037193230.grb'),
                              parameter=parameter)

    # reading returns an image object which contains a data dictionary
    # with one array per parameter. The returned data is a global 0.25 degree
    # image/array.
    image = img.read()

    assert image.data['086_L1'].shape == (720, 1440)
    assert image.lon[0, 0] == -179.875
    assert image.lon[0, 1439] == 179.875
    assert image.lat[0, 0] == 89.875
    assert image.lat[719, 0] == -89.875
    assert sorted(image.data.keys()) == sorted(parameter)
    assert image.data['086_L1'][26, 609] == 30.7344
    assert image.data['086_L2'][26, 609] == 93.138
    assert image.data['085_L1'][576, 440] == 285.19
    assert image.data['138'][26, 609] == 237.27
    assert image.data['051'][26, 609] == 0
    assert image.lon.shape == (720, 1440)
    assert image.lon.shape == image.lat.shape

Reading by date
~~~~~~~~~~~~~~~

All the gldas data in a directory structure can be accessed by date.
The filename is automatically built from the given date.

.. code-block:: python

    from gldas.interface import GLDAS_Noah_v1_025Ds

    parameter = ['086_L2', '086_L1', '085_L1', '138', '132', '051']
    img = GLDAS_Noah_v1_025Ds(data_path=os.path.join(os.path.dirname(__file__),
                                                    'test-data',
                                                    'GLDAS_NOAH_image_data'),
                              parameter=parameter)

    image = img.read(datetime(2015, 1, 1, 0))


For reading all image between two dates the
:py:meth:`gldas.interface.GLDAS_Noah_v1_025Ds.iter_images` iterator can be
used.
