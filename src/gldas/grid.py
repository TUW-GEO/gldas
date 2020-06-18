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
from netCDF4 import Dataset
import os

def subgrid4bbox(grid, min_lon, min_lat, max_lon, max_lat):
    gpis, lons, lats, _ = grid.get_grid_points()
    assert len(gpis) == len(lats) == len(lons)
    bbox_gpis = gpis[np.where((lons <= max_lon) & (lons >= min_lon) &
                              (lats <= max_lat) & (lats >= min_lat))]

    return grid.subgrid_from_gpis(bbox_gpis)


def GLDAS025Grids(only_land=False):
    """
    Create global 0.25 DEG gldas grids (origin in bottom left)

    Parameters
    ---------
    only_land : bool, optional (default: False)
        Uses the land mask to reduce the GLDAS 0.25DEG land grid to land points
        only.

    Returns
    --------
    grid : pygeogrids.CellGrid
        Either a land grid or a global grid
    """

    resolution = 0.25
    glob_lons = np.arange(-180 + resolution / 2, 180 + resolution / 2, resolution)
    glob_lats = np.arange(-90 + resolution / 2, 90 + resolution / 2, resolution)
    lon, lat = np.meshgrid(glob_lons, glob_lats)
    glob_grid = BasicGrid(lon.flatten(), lat.flatten()).to_cell_grid(cellsize=5.)

    if only_land:
        ds = Dataset(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                  'GLDASp4_landmask_025d.nc4'))
        land_lats = ds.variables['lat'][:]
        land_mask = ds.variables['GLDAS_mask'][:].flatten().filled() == 0.
        dlat = glob_lats.size - land_lats.size

        land_mask = np.concatenate((np.ones(dlat * glob_lons.size), land_mask))
        land_points = np.ma.masked_array(glob_grid.get_grid_points()[0], land_mask)

        land_grid = glob_grid.subgrid_from_gpis(land_points[~land_points.mask].filled())
        return land_grid
    else:
        return glob_grid


def GLDAS025Cellgrid():
    return GLDAS025Grids(only_land=False)


def GLDAS025LandGrid():
    return GLDAS025Grids(only_land=True)


if __name__ == '__main__':
    GLDAS025LandGrid()


def load_grid(land_points=True, bbox=None):
    """
    Load gldas grid.

    Parameters
    ----------
    land_points : bool, optional (default: True)
        Reshuffle only land points
    bbox : tuple, optional (default: True)
        (min_lat, min_lon, max_lat, max_lon)
        Bounding box to limit reshuffling to.
    """
    if land_points:
        subgrid = GLDAS025LandGrid()
        if bbox is not None:
            subgrid = subgrid4bbox(subgrid, *bbox)
    else:
        if bbox is not None:
            subgrid = subgrid4bbox(GLDAS025Cellgrid(), *bbox)
        else:
            subgrid = None

    return subgrid