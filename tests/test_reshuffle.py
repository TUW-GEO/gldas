import os
import glob
import tempfile
import numpy as np
import numpy.testing as nptest

from gldas.reshuffle import main
from gldas.interface import GLDASTs

from tempfile import TemporaryDirectory

import pytest


@pytest.mark.parametrize(
    "landpoints,bbox,n_files_should",
    # 15 cells, 4 with out landpoints, 1 grid file
    [(True, True, 15-4+1), (False, True, 15+1)],
)
def test_reshuffle(landpoints, bbox, n_files_should):
    if bbox is True:
        bbox = ["41.125", "11.125", "63.875", "23.875"]
    inpath = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "test-data",
        "img2ts_test",
        "netcdf",
    )
    startdate = "2016-01-01T03:00"
    enddate = "2016-01-01T21:00"
    parameters = ["SoilMoi0_10cm_inst", "SoilMoi10_40cm_inst"]

    with TemporaryDirectory() as ts_path:
        args = (
            [inpath, ts_path, startdate, enddate]
            + parameters
            + ["--land_points", str(landpoints)]
        )
        if bbox:
            args += ["--bbox", *bbox]
        main(args)
        assert len(glob.glob(os.path.join(ts_path, "*.nc"))) == n_files_should

        ds = GLDASTs(
            ts_path,
            ioclass_kws={"read_bulk": True, "read_dates": False},
            parameters=["SoilMoi0_10cm_inst", "SoilMoi10_40cm_inst"],
        )

        ts = ds.read(45.08, 15.1)
        ts_SM0_10_values_should = np.array(
            [9.595, 9.593, 9.578, 9.562, 9.555, 9.555, 9.556], dtype=np.float32
        )
        nptest.assert_allclose(
            ts["SoilMoi0_10cm_inst"].values, ts_SM0_10_values_should, rtol=1e-5
        )
        ts_SM10_40_values_should = np.array(
            [50.065, 50.064, 50.062, 50.060, 50.059, 50.059, 50.059],
            dtype=np.float32,
        )
        nptest.assert_allclose(
            ts["SoilMoi10_40cm_inst"].values, ts_SM10_40_values_should, rtol=1e-5
        )
        ds.close()
