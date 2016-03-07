import os

from datetime import datetime

from rs_data_readers.GLDAS_NOAH.interface import GLDAS025Ds


def test_GLDAS025Img_img_reading():

    parameter = ['086_L2', '086_L1', '085_L1', '138', '132', '051']
    img = GLDAS025Ds(data_path=os.path.join(os.path.dirname(__file__),
                                            '..', 'test-data',
                                            'GLDAS_NOAH_image_data'),
                     parameter=parameter)

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
