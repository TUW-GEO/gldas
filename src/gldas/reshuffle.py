# The MIT License (MIT)
#
# Copyright (c) 2018, TU Wien
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Module for a command line interface to convert the GLDAS data into a
time series format using the repurpose package
"""

import os
import sys
import argparse
from datetime import datetime

from pygeogrids import BasicGrid

from repurpose.img2ts import Img2Ts
from gldas.interface import GLDAS_Noah_v1_025Ds, GLDAS_Noah_v21_025Ds
from gldas.grid import load_grid
import warnings


def get_filetype(inpath):
    """
    Tries to find out the file type by searching for
    grib or nc files two subdirectories into the passed input path.
    If function fails, netcdf is assumed.

    Parameters
    ----------
    input_root: str
        Input path where GLDAS data was downloaded

    Returns
    -------
    filetype : str
        File type string.
    """
    onedown = os.path.join(inpath, os.listdir(inpath)[0])
    twodown = os.path.join(onedown, os.listdir(onedown)[0])

    filelist = []
    for path, subdirs, files in os.walk(twodown):
        for name in files:
            filename, extension = os.path.splitext(name)
            filelist.append(extension)

    if ".nc4" in filelist and ".grb" not in filelist:
        return "netCDF"
    elif ".grb" in filelist and ".nc4" not in filelist:
        return "grib"
    else:
        # if file type cannot be detected, guess netCDF
        return "netCDF"


def mkdate(datestring):
    """
    Create date string.

    Parameters
    ----------
    datestring : str
        Date string.

    Returns
    -------
    datestr : datetime
        Date string as datetime.
    """
    if len(datestring) == 10:
        return datetime.strptime(datestring, "%Y-%m-%d")
    if len(datestring) == 16:
        return datetime.strptime(datestring, "%Y-%m-%dT%H:%M")


def str2bool(val):
    if val in ["True", "true", "t", "T", "1"]:
        return True
    else:
        return False


def reshuffle(
    input_root,
    outputpath,
    startdate,
    enddate,
    parameters,
    input_grid=None,
    imgbuffer=50,
):
    """
    Reshuffle method applied to GLDAS data.

    Parameters
    ----------
    input_root: string
        input path where gldas data was downloaded
    outputpath : string
        Output path.
    startdate : datetime
        Start date.
    enddate : datetime
        End date.
    parameters: list
        parameters to read and convert
    input_grid : CellGrid, optional (default: None)
        Local input grid to read data for. If None is passed, we create the grid
        from data.
    imgbuffer: int, optional
        How many images to read at once before writing time series.
    """

    if get_filetype(input_root) == "grib":
        if input_grid is not None:
            warnings.warn("Land Grid is fit to GLDAS 2.x netCDF data")

        input_dataset = GLDAS_Noah_v1_025Ds(
            input_root, parameters, subgrid=input_grid, array_1D=True
        )
    else:
        input_dataset = GLDAS_Noah_v21_025Ds(
            input_root, parameters, subgrid=input_grid, array_1D=True
        )

    if not os.path.exists(outputpath):
        os.makedirs(outputpath)

    global_attr = {"product": "GLDAS"}

    # get time series attributes from first day of data.
    data = input_dataset.read(startdate)
    ts_attributes = data.metadata
    if input_grid is None:
        grid = BasicGrid(data.lon, data.lat)
    else:
        grid = input_grid

    reshuffler = Img2Ts(
        input_dataset=input_dataset,
        outputpath=outputpath,
        startdate=startdate,
        enddate=enddate,
        input_grid=grid,
        imgbuffer=imgbuffer,
        cellsize_lat=5.0,
        cellsize_lon=5.0,
        global_attr=global_attr,
        zlib=True,
        unlim_chunksize=1000,
        ts_attributes=ts_attributes,
    )
    reshuffler.calc()


def parse_args(args):
    """
    Parse command line parameters for recursive download.

    Parameters
    ----------
    args : list of str
        Command line parameters as list of strings.

    Returns
    -------
    args : argparse.Namespace
        Command line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Convert GLDAS data to time series format."
    )
    parser.add_argument(
        "dataset_root",
        help="Root of local filesystem where the " "data is stored.",
    )

    parser.add_argument(
        "timeseries_root",
        help="Root of local filesystem where the timeseries "
        "should be stored.",
    )

    parser.add_argument(
        "start",
        type=mkdate,
        help=(
            "Startdate. Either in format YYYY-MM-DD or " "YYYY-MM-DDTHH:MM."
        ),
    )

    parser.add_argument(
        "end",
        type=mkdate,
        help=("Enddate. Either in format YYYY-MM-DD or " "YYYY-MM-DDTHH:MM."),
    )

    parser.add_argument(
        "parameters",
        metavar="parameters",
        nargs="+",
        help=(
            "Parameters to reshuffle into time series format. "
            "e.g. SoilMoi0_10cm_inst SoilMoi10_40cm_inst for "
            "Volumetric soil water layers 1 to 2."
        ),
    )

    parser.add_argument(
        "--land_points",
        type=str2bool,
        default="False",
        help=(
            "Set True to convert only land points as defined"
            " in the GLDAS land mask (faster and less/smaller files)"
        ),
    )

    parser.add_argument(
        "--bbox",
        type=float,
        default=None,
        nargs=4,
        help=(
            "min_lon min_lat max_lon max_lat. "
            "Bounding Box (lower left and upper right corner) "
            "of area to reshuffle (WGS84)"
        ),
    )

    parser.add_argument(
        "--imgbuffer",
        type=int,
        default=50,
        help=(
            "How many images to read at once. Bigger "
            "numbers make the conversion faster but "
            "consume more memory."
        ),
    )

    args = parser.parse_args(args)
    # set defaults that can not be handled by argparse

    print(
        "Converting data from {} to"
        " {} into folder {}.".format(
            args.start.isoformat(), args.end.isoformat(), args.timeseries_root
        )
    )

    return args


def main(args):
    """
    Main routine used for command line interface.

    Parameters
    ----------
    args : list of str
        Command line arguments.
    """
    args = parse_args(args)

    input_grid = load_grid(
        land_points=args.land_points,
        bbox=tuple(args.bbox) if args.bbox is not None else None,
    )

    reshuffle(
        args.dataset_root,
        args.timeseries_root,
        args.start,
        args.end,
        args.parameters,
        input_grid=input_grid,
        imgbuffer=args.imgbuffer,
    )


def run():
    main(sys.argv[1:])
