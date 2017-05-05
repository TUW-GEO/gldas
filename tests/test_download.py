"""
Tests for the download module of GLDAS.
"""
import os
from datetime import datetime
from gldas.download import get_last_formatted_dir_in_dir
from gldas.download import get_first_formatted_dir_in_dir
from gldas.download import get_last_gldas_folder
from gldas.download import get_first_gldas_folder
from gldas.download import gldas_folder_get_version_first_last

def test_get_last_dir_in_dir():
    path = os.path.join(os.path.dirname(__file__),
                        'folder_test', 'success')
    last_dir = get_last_formatted_dir_in_dir(path, "{:%Y}")
    assert last_dir == '2014'

def test_get_last_dir_in_dir_failure():
    path = os.path.join(os.path.dirname(__file__),
                        'folder_test', 'failure')
    last_dir = get_last_formatted_dir_in_dir(path, "{:%Y}")
    assert last_dir == None


def test_get_first_dir_in_dir():
    path = os.path.join(os.path.dirname(__file__),
                        'folder_test', 'success')
    last_dir = get_first_formatted_dir_in_dir(path, "{:%Y}")
    assert last_dir == '2013'

def test_get_last_gldas_folder():
    path = os.path.join(os.path.dirname(__file__),
                        'folder_test', 'success')
    last = get_last_gldas_folder(path, ['{:%Y}', '{:%j}'])
    last_should = os.path.join(path, "2014", "134")
    assert last == last_should

def test_get_last_gldas_folder_no_folder():
    path = os.path.join(os.path.dirname(__file__),
                        'folder_test', 'failure')
    last = get_last_gldas_folder(path, ['{:%Y}', '{:%j}'])
    last_should = None
    assert last == last_should

def test_get_first_gldas_folder():
    path = os.path.join(os.path.dirname(__file__),
                        'folder_test', 'success')
    last = get_first_gldas_folder(path, ['{:%Y}', '{:%j}'])
    last_should = os.path.join(path, "2013", "001")
    assert last == last_should

def test_get_first_gldas_folder_no_folder():
    path = os.path.join(os.path.dirname(__file__),
                        'folder_test', 'failure')
    last = get_first_gldas_folder(path, ['{:%Y}', '{:%j}'])
    last_should = None
    assert last == last_should

def test_gldas_get_start_end():
    path = os.path.join(os.path.dirname(__file__),
                        'test-data', 'GLDAS_NOAH_image_data')
    version, start, end = gldas_folder_get_version_first_last(path)
    version_should='GLDAS_Noah_v21_025'
    start_should = datetime(2015,1,1)
    end_should = datetime(2015,1,1)
    assert version == version_should
    assert end == end_should
    assert start == start_should
    
