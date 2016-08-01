import os

from datetime import datetime

from gldas.interface import GLDAS_Noah_v1_025Ds
from gldas.interface import GLDAS_Noah_v1_025Img


def test_GLDAS_Noah_v1_025Ds_img_reading():

    parameter = ['086_L2', '086_L1', '085_L1', '138', '132', '051']
    img = GLDAS_Noah_v1_025Ds(data_path=os.path.join(os.path.dirname(__file__),
                                                     'test-data',
                                                     'GLDAS_NOAH_image_data'),
                              parameter=parameter,
                              array_1D=True)

    image = img.read(
        datetime(2015, 1, 1, 0))

    assert sorted(image.data.keys()) == sorted(parameter)
    assert image.timestamp == datetime(2015, 1, 1, 0)
    assert image.data['086_L1'][998529] == 30.7344
    assert image.data['086_L2'][998529] == 93.138
    assert image.data['085_L1'][206360] == 285.19
    assert image.data['138'][998529] == 237.27
    assert image.data['051'][998529] == 0
    assert image.lon.shape == (360 * 180 * (1 / 0.25)**2,)
    assert image.lon.shape == image.lat.shape


def test_GLDAS_Noah_v1_025Img_img_reading_1D():

    parameter = ['086_L2', '086_L1', '085_L1', '138', '132', '051']
    img = GLDAS_Noah_v1_025Img(os.path.join(os.path.dirname(__file__),
                                            'test-data',
                                            'GLDAS_NOAH_image_data',
                                            '2015',
                                            '001',
                                            'GLDAS_NOAH025SUBP_3H.A2015001.0000.001.2015037193230.grb'),
                               parameter=parameter,
                               array_1D=True)

    image = img.read()

    assert sorted(image.data.keys()) == sorted(parameter)
    assert image.data['086_L1'][998529] == 30.7344
    assert image.data['086_L2'][998529] == 93.138
    assert image.data['085_L1'][206360] == 285.19
    assert image.data['138'][998529] == 237.27
    assert image.data['051'][998529] == 0
    assert image.lon.shape == (360 * 180 * (1 / 0.25)**2,)
    assert image.lon.shape == image.lat.shape

def test_GLDAS_Noah_v1_025Img_img_reading_2D():

    parameter = ['086_L2', '086_L1', '085_L1', '138', '132', '051']
    img = GLDAS_Noah_v1_025Img(os.path.join(os.path.dirname(__file__),
                                            'test-data',
                                            'GLDAS_NOAH_image_data',
                                            '2015',
                                            '001',
                                            'GLDAS_NOAH025SUBP_3H.A2015001.0000.001.2015037193230.grb'),
                               parameter=parameter)

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
