
import os
import glob
import tempfile
import numpy as np
import numpy.testing as nptest

from gldas.reshuffle import main
from gldas.interface import GLDASTs


def test_reshuffle():

    inpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "test-data", "img2ts_test")
    ts_path = tempfile.mkdtemp()
    startdate = "2015-01-01"
    enddate = "2015-01-01"
    parameters = ["085_L1", "085_L2"]

    args = [inpath, ts_path, startdate, enddate] + parameters
    main(args)
    assert len(glob.glob(os.path.join(ts_path, "*.nc"))) == 2593
    ds = GLDASTs(ts_path)
    ts = ds.read_ts(45, 15)
    ts_L1_values_should = np.array([280.75, 278.68, 284.34, 294.94,
                                    299.36, 294.51, 287.93, 283.49], dtype=np.float32)
    nptest.assert_allclose(ts['085_L1'].values, ts_L1_values_should)
    ts_L2_values_should = np.array([288.96, 288.48, 288.09, 288.3,
                                    288.92, 289.43, 289.52, 289.3], dtype=np.float32)
    nptest.assert_allclose(ts['085_L2'].values, ts_L2_values_should)
