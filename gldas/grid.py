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

import numpy as np

from pygeogrids.grids import BasicGrid
import pandas as pd


def GLDAS025Cellgrid():
    '''
    GLDAS-Noah 0.25deg cell grid.
    :return: global QDEG-CellGrid
    '''
    resolution = 0.25
    lon, lat = np.meshgrid(
        np.arange(-180 + resolution / 2, 180 + resolution / 2, resolution),
        np.arange(-90 + resolution / 2, 90 + resolution / 2, resolution))

    return BasicGrid(lon.flatten(), lat.flatten()).to_cell_grid(cellsize=5.)


def GLDASLandPoints(grid):
    '''
    Load land mask from https://ldas.gsfc.nasa.gov/gldas/data/0.25deg/landmask_mod44w_025.asc
    and reduce input grid to land points
    :return: (GPI, dist)
    '''
    try:
        land_mask = pd.read_csv('https://ldas.gsfc.nasa.gov/gldas/data/0.25deg/landmask_mod44w_025.asc',
                                delim_whitespace=True, header=None, names=['idx', 'gpi', 'lat', 'lon', 'land_flag'])
    except:
        raise ImportError(
            'reading land mask from https://ldas.gsfc.nasa.gov/gldas/data/0.25deg/landmask_mod44w_025.asc failed.')
    land_mask = land_mask.loc[land_mask['land_flag'] == 1]
    lat, lon = land_mask['lat'].values, land_mask['lon'].values

    return grid.find_nearest_gpi(lon, lat)


def GLDAS025LandGrid():
    '''
    0.25deg cell grid of land points from gldas land mask.
    :return: global QDEG-LandGrid
    '''
    grid = GLDAS025Cellgrid()
    land_gpis, dist = GLDASLandPoints(grid)
    if any(dist) > 0:
        raise Exception('GLDAS grid does not conform with QDEG grid')
    return grid.subgrid_from_gpis(land_gpis)
