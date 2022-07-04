import numpy as np
from pygeogrids.grids import BasicGrid
from netCDF4 import Dataset
import os

def subgrid4bbox(grid, min_lon, min_lat, max_lon, max_lat):
    """
    Select a spatial subset for the grid by bound box corner points

    Parameters
    ----------
    grid: BasicGrid or CellGrid
        Grid object to trim.
    min_lon: float
        Lower left corner longitude
    min_lat: float
        Lower left corner latitude
    max_lon: float
        Upper right corner longitude
    max_lat: float
        Upper right corner latitude

    Returns
    -------
    subgrid: BasicGrid or CellGrid
        Subset of the input grid.
    """
    gpis, lons, lats, _ = grid.get_grid_points()
    assert len(gpis) == len(lats) == len(lons)
    bbox_gpis = gpis[
        np.where(
            (lons <= max_lon)
            & (lons >= min_lon)
            & (lats <= max_lat)
            & (lats >= min_lat)
        )
    ]

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
    glob_lons = np.arange(
        -180 + resolution / 2, 180 + resolution / 2, resolution
    )
    glob_lats = np.arange(
        -90 + resolution / 2, 90 + resolution / 2, resolution
    )
    lon, lat = np.meshgrid(glob_lons, glob_lats)
    glob_grid = BasicGrid(lon.flatten(), lat.flatten()).to_cell_grid(
        cellsize=5.0
    )

    if only_land:
        ds = Dataset(
            os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                "GLDASp4_landmask_025d.nc4",
            )
        )
        land_lats = ds.variables["lat"][:]
        land_mask = ds.variables["GLDAS_mask"][:].flatten().filled() == 0.0
        dlat = glob_lats.size - land_lats.size

        land_mask = np.concatenate((np.ones(dlat * glob_lons.size), land_mask))
        land_points = np.ma.masked_array(
            glob_grid.get_grid_points()[0], land_mask
        )

        land_grid = glob_grid.subgrid_from_gpis(
            land_points[~land_points.mask].filled()
        )
        return land_grid
    else:
        return glob_grid


def GLDAS025Cellgrid():
    """Alias to create a global 0.25 DEG grid without gaps w. 5 DEG cells """
    return GLDAS025Grids(only_land=False)


def GLDAS025LandGrid():
    """Alias to create a global 0.25 DEG grid over land only w. 5 DEG cells """
    return GLDAS025Grids(only_land=True)

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
