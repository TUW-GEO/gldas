import os

from datetime import datetime

from rs_data_readers.GLDAS_NOAH.interface import GLDAS025Img


def test_GLDAS025Img_img_reading():

    parameter = ['086_L2', '086_L1', '085_L1', '138', '132', '051']
    img = GLDAS025Img(data_path=os.path.join(os.path.dirname(__file__),
                                             'image_data'),
                      parameter=parameter)

    data, metadata, timestamp, lon, lat, time = img.read_img(datetime(2015, 1, 1, 0))

    assert sorted(data.keys()) == sorted(parameter)
    assert timestamp == datetime(2015, 1, 1, 0)
    assert data['086_L1'][998529] == 30.7344
    assert data['086_L2'][998529] == 93.138
    assert data['085_L1'][206360] == 285.19
    assert data['138'][998529] == 237.27
    assert data['051'][998529] == 0
    assert lon.shape == (360 * 180 * (1/0.25)**2,)
    assert lon.shape == lat.shape
