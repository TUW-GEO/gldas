import numpy as np

from pygeogrids.grids import BasicGrid
import pandas as pd

def GLDAS025Cellgrid():
    """
    Class for the GLDAS-Noah Version1 0.25deg cell grid.
    """

    resolution = 0.25

    lon, lat = np.meshgrid(
        np.arange(-180 + resolution/2, 180 + resolution/2, resolution),
        np.arange(-90 + resolution/2, 90 + resolution/2, resolution))

    return BasicGrid(lon.flatten(), lat.flatten()).to_cell_grid(cellsize=5.)

def GLDASLandPoints(grid):
    '''
    Load land mask from https://ldas.gsfc.nasa.gov/gldas/data/0.25deg/landmask_mod44w_025.asc
    and reduce input grid to land points
    :return: land grid
    '''
    land_mask = pd.read_csv('https://ldas.gsfc.nasa.gov/gldas/data/0.25deg/landmask_mod44w_025.asc',
                            delim_whitespace=True, header=None, names=['idx', 'gpi', 'lat', 'lon', 'land_flag'])
    land_mask = land_mask.loc[land_mask['land_flag'] == 1]
    lat, lon = land_mask['lat'].values, land_mask['lon'].values

    return grid.find_nearest_gpi(lon,lat)

def GLDAS025LandGrid():
    """
    Class for the GLDAS-Noah Version1 0.25deg cell grid of land points from gldas land mask.
    """
    grid = GLDAS025Cellgrid()
    land_gpis, dist = GLDASLandPoints(grid)
    if any(dist) > 0:
        raise Exception('GLDAS grid does not conform with QDEG grid')
    return grid.subgrid_from_gpis(land_gpis)