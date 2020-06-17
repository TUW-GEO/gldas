# -*- coding: utf-8 -*-

"""
Module description
"""
# TODO:
#   (+) 
#---------
# NOTES:
#   -

from gldas.reshuffle import reshuffle
from pygeogrids.netcdf import load_grid
import os
from datetime import datetime
from pygeogrids.grids import CellGrid

input_root = "/home/wpreimes/shares/radar/Datapool/GLDAS/01_raw/GLDAS_NOAH025_3H.2.1/datasets/netcdf"
startdate, enddate = datetime(2000,1,1,3,0), datetime(2019,12,31)
parameters = ['ECanop_tavg', 'ESoil_tavg', 'Evap_tavg', 'Tveg_tavg', 'Qsb_acc', 'SoilMoi0_10cm_int', 'Rainf_f_tavg',
              'AvgSurfT_inst']

for country in ['Austria', 'Morocco', 'Senegal', 'Mozambique']:
    outputpath = "/home/wpreimes/shares/users/users_temp/gldas/{}".format(country)
    grid = load_grid(os.path.join(outputpath, f'grid_{country}.nc'))
    gpis, lons, lats, cells = grid.get_grid_points()
    grid = CellGrid(lon=lons.filled(), lat=lats.filled(), gpis=gpis.filled(),
                    cells=cells.filled())


    reshuffle(input_root=input_root, outputpath=outputpath, startdate=startdate,
              enddate=enddate, parameters=parameters, input_grid=grid, imgbuffer=1000)
