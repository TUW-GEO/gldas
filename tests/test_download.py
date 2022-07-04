"""
Tests for the download module of GLDAS.
"""
import os
import unittest
from datetime import datetime
import pytest
import tempfile

from gldas.download import get_last_formatted_dir_in_dir
from gldas.download import get_first_formatted_dir_in_dir
from gldas.download import get_last_gldas_folder
from gldas.download import get_first_gldas_folder
from gldas.download import gldas_folder_get_version_first_last
from gldas.download import main as main_download

from gldas.interface import GLDAS_Noah_v21_025Ds

try:
    username = os.environ['GES_DISC_USERNAME']
    pwd = os.environ['GES_DISC_PWD']
except KeyError:
    username = pwd = None

@pytest.mark.skipif(username is None or pwd is None,
                    reason="Environment variable (or GitHub Secret) expected but not found:"
                           "`GES_DISC_USERNAME` and/or `GES_DISC_PWD`")
class TestDownload(unittest.TestCase):
    def setUp(self) -> None:
        self.outpath = tempfile.mkdtemp(prefix='gldas')

    def test_download_GLDAS_Noah_v21_025(self):
        args = [self.outpath, '-s', '2010-03-02', '-e' '2010-03-02', '--product', "GLDAS_Noah_v21_025",
               '--username', username, '--password', pwd]
        main_download(args)
        assert len(os.listdir(os.path.join(self.outpath, '2010', '061'))) == 8 * 2 + 2

        ds = GLDAS_Noah_v21_025Ds(self.outpath)
        img = ds.read(datetime(2010, 3, 2, 3))
        assert list(img.data.keys()) == ['SoilMoi0_10cm_inst'] == list(img.metadata.keys())
        ds.close()


def test_get_last_dir_in_dir():
    path = os.path.join(os.path.dirname(__file__), "folder_test", "success")
    last_dir = get_last_formatted_dir_in_dir(path, "{time:%Y}")
    assert last_dir == "2014"


def test_get_last_dir_in_dir_failure():
    path = os.path.join(os.path.dirname(__file__), "folder_test", "failure")
    last_dir = get_last_formatted_dir_in_dir(path, "{time:%Y}")
    assert last_dir == None


def test_get_first_dir_in_dir():
    path = os.path.join(os.path.dirname(__file__), "folder_test", "success")
    last_dir = get_first_formatted_dir_in_dir(path, "{time:%Y}")
    assert last_dir == "2013"


def test_get_last_gldas_folder():
    path = os.path.join(os.path.dirname(__file__), "folder_test", "success")
    last = get_last_gldas_folder(path, ["{time:%Y}", "{time:%j}"])
    last_should = os.path.join(path, "2014", "134")
    assert last == last_should


def test_get_last_gldas_folder_no_folder():
    path = os.path.join(os.path.dirname(__file__), "folder_test", "failure")
    last = get_last_gldas_folder(path, ["{time:%Y}", "{time:%j}"])
    last_should = None
    assert last == last_should


def test_get_first_gldas_folder():
    path = os.path.join(os.path.dirname(__file__), "folder_test", "success")
    last = get_first_gldas_folder(path, ["{time:%Y}", "{time:%j}"])
    last_should = os.path.join(path, "2013", "001")
    assert last == last_should


def test_get_first_gldas_folder_no_folder():
    path = os.path.join(os.path.dirname(__file__), "folder_test", "failure")
    last = get_first_gldas_folder(path, ["{time:%Y}", "{time:%j}"])
    last_should = None
    assert last == last_should


def test_gldas_get_start_end():
    path = os.path.join(
        os.path.dirname(__file__), "test-data", "GLDAS_NOAH_image_data"
    )
    version, start, end = gldas_folder_get_version_first_last(path)
    version_should = "GLDAS_Noah_v21_025"
    start_should = datetime(2015, 1, 1)
    end_should = datetime(2015, 1, 1)
    assert version == version_should
    assert end == end_should
    assert start == start_should

