# -*- coding: utf-8 -*-

import warnings
import numpy as np
import os

try:
    import pygrib
except ImportError:
    warnings.warn("pygrib has not been imported")

from pygeobase.io_base import ImageBase, MultiTemporalImageBase
from pygeobase.object_base import Image
import pygeogrids
from pynetcf.time_series import GriddedNcOrthoMultiTs

from datetime import timedelta

from gldas.grid import GLDAS025Cellgrid
from netCDF4 import Dataset

class GLDAS_Noah_v21_025Img(ImageBase):
    """
    Class for reading one GLDAS Noah v2.1 nc file in 0.25° grid.

    Parameters
    ----------
    filename: string
        filename of the GLDAS nc file
    mode: string, optional
        mode of opening the file, only 'r' is implemented at the moment
    parameter : string or list, optional
        one or list of parameters to read, see GLDAS v2.1 documentation for more information
        Default : 'SoilMoi0_10cm_inst'
    array_1D: boolean, optional
        if set then the data is read into 1D arrays. Needed for some legacy code.
    """
    
    def __init__(self, filename, mode='r', parameter='SoilMoi0_10cm_inst', array_1D=False):
        super(GLDAS_Noah_v21_025Img, self).__init__(filename, mode=mode)

        if type(parameter) != list:
            parameter = [parameter]
        self.parameters = parameter
        self.fill_values = np.repeat(9999., 1440 * 120)
        self.grid = GLDAS025Cellgrid()
        self.array_1D = array_1D
    
    def read(self, timestamp=None):
        
        #print 'read file: %s' %self.filename
        #Returns the selected parameters for a gldas image and according metadata
        return_img = {}
        return_metadata = {}
        
        try:
            dataset = Dataset(self.filename)
        except IOError as e:
            print(e)
            print(" ".join([self.filename, "can not be opened"]))
            raise e
         

        param_names=[]
        for parameter in self.parameters:
            param_names.append(parameter)
            
        
        for parameter, variable in dataset.variables.items():
            if parameter in param_names:
                param_metadata={}
                param_data={}           
                for attrname in variable.ncattrs():
                    if attrname in ['long_name','units']:
                        param_metadata.update({str(attrname):getattr(variable,attrname)})
                        
                   
                param_data=dataset.variables[parameter][:]
                np.ma.set_fill_value(param_data,9999)  
                
                param_data=np.concatenate((self.fill_values,
                                           np.ma.getdata(param_data.filled())
                                           .flatten()))
                                        
                return_img.update({str(parameter):param_data[self.grid.activegpis]})
                return_metadata.update({str(parameter):param_metadata})
                        
            #Check for corrupt files
                try:
                    return_img[parameter]
                except KeyError:
                    path, thefile = os.path.split(self.filename)
                    print ('%s in %s is corrupt - filling image with NaN values' %(parameter,thefile))
                    return_img[parameter]  = np.empty(self.grid.n_gpi).fill(np.nan)
                    return_metadata['corrupt_parameters'].append()
                    
        dataset.close()
        if self.array_1D:
            return Image(self.grid.activearrlon,
                         self.grid.activearrlat,
                         return_img,
                         return_metadata,
                         timestamp)
        else:
            for key in return_img:
                return_img[key]=np.flipud(return_img[key].reshape((720,1440)))
            
            return Image(np.flipud(self.grid.activearrlon.reshape((720,1440))),
                         np.flipud(self.grid.activearrlat.reshape((720,1440))),
                         return_img, 
                         return_metadata,
                         timestamp)
                        
                
    def write(self,data):
        raise NotImplementedError()
        
    def flush(self):
        pass
    
    def close(self):
        pass

class GLDAS_Noah_v1_025Img(ImageBase):
    """
    Class for reading one GLDAS Noah v1 grib file in 0.25° grid.

    Parameters
    ----------
    filename: string
        filename of the GLDAS grib file
    mode: string, optional
        mode of opening the file, only 'r' is implemented at the moment
    parameter : string or list, optional
        one or list of ['001', '011', '032', '051', '057', '065', '071',
                        '085_L1', '085_L2', '085_L3', '085_L4',
                        '086_L1', '086_L2', '086_L3', '086_L4',
                        '099', '111', '112', '121', '122', '131', '132', '138',
                        '155', '204', '205', '234', '235']
        parameters to read, see GLDAS documentation for more information
        Default : '086_L1'
    array_1D: boolean, optional
        if set then the data is read into 1D arrays. Needed for some legacy code.
    """

    def __init__(self, filename, mode='r', parameter='086_L1', array_1D=False):
        super(GLDAS_Noah_v1_025Img, self).__init__(filename, mode=mode)

        if type(parameter) != list:
            parameter = [parameter]
        self.parameters = parameter
        self.fill_values = np.repeat(9999., 1440 * 120)
        self.grid = GLDAS025Cellgrid()
        self.array_1D = array_1D

    def read(self, timestamp=None):

        return_img = {}
        return_metadata = {}
        layers = {'085': 1, '086': 1}

        try:
            grbs = pygrib.open(self.filename)
        except IOError as e:
            print(e)
            print(" ".join([self.filename, "can not be opened"]))
            raise e

        ids = []
        for parameter in self.parameters:
            ids.append(int(parameter.split('_')[0]))
        parameter_ids = np.unique(np.array(ids))

        for message in grbs:
            if message['indicatorOfParameter'] in parameter_ids:
                parameter_id = '{:03d}'.format(message['indicatorOfParameter'])

                param_metadata = {}
                # read metadata in any case
                param_metadata['units'] = message['units']
                param_metadata['long_name'] = message['parameterName']

                if parameter_id in layers.keys():
                    parameter = '_'.join((parameter_id, 'L' +
                                          str(layers[parameter_id])))

                    if parameter in self.parameters:
                        param_data = np.concatenate((
                            self.fill_values,
                            np.ma.getdata(message['values']).flatten()))

                        return_img[parameter] = param_data[
                            self.grid.activegpis]
                        return_metadata[parameter] = param_metadata
                    layers[parameter_id] += 1

                else:
                    parameter = parameter_id
                    param_data = np.concatenate((
                        self.fill_values,
                        np.ma.getdata(message['values']).flatten()))
                    return_img[parameter] = param_data[self.grid.activegpis]
                    return_metadata[parameter] = param_metadata

        grbs.close()
        for parameter in self.parameters:
            try:
                return_img[parameter]
            except KeyError:
                print(self.filename[self.filename.rfind('GLDAS'):],
                      'corrupt file - filling image with nan values')
                return_img[parameter] = np.empty(self.grid.n_gpi)
                return_img[parameter].fill(np.nan)

        if self.array_1D:
            return Image(self.grid.activearrlon,
                         self.grid.activearrlat,
                         return_img,
                         return_metadata,
                         timestamp)
        else:
            for key in return_img:
                return_img[key] = np.flipud(
                    return_img[key].reshape((720, 1440)))

            return Image(np.flipud(self.grid.activearrlon.reshape((720, 1440))),
                         np.flipud(
                             self.grid.activearrlat.reshape((720, 1440))),
                         return_img,
                         return_metadata,
                         timestamp)

    def write(self, data):
        raise NotImplementedError()

    def flush(self):
        pass

    def close(self):
        pass


class GLDAS_Noah_v21_025Ds(MultiTemporalImageBase):
    """
    Class for reading GLDAS v2.1 images in nc format.

    Parameters
    ----------
    data_path : string
        path to the nc files
    parameter : string or list, optional
        one or list of parameters to read, see GLDAS v2.1 documentation for more information
        Default : 'SoilMoi0_10cm_inst'
    array_1D: boolean, optional
        if set then the data is read into 1D arrays. Needed for some legacy code.
    """

    def __init__(self, data_path, parameter='SoilMoi0_10cm_inst', array_1D=False):

        ioclass_kws = {'parameter': parameter,
                       'array_1D': array_1D}

        sub_path = ['%Y','%j']
        filename_templ = "GLDAS_NOAH025_3H.A{datetime}.*.nc4"
        super(GLDAS_Noah_v21_025Ds, self).__init__(data_path, GLDAS_Noah_v21_025Img,
                                                  fname_templ=filename_templ,
                                                  datetime_format="%Y%m%d.%H%M",
                                                  subpath_templ=sub_path,
                                                  exact_templ=False,
                                                  ioclass_kws=ioclass_kws)
        
    

    def tstamps_for_daterange(self, start_date, end_date):
        """
        return timestamps for daterange,

        Parameters
        ----------
        start_date: datetime
            start of date range
        end_date: datetime
            end of date range

        Returns
        -------
        timestamps : list
            list of datetime objects of each available image between
            start_date and end_date
        """
        img_offsets = np.array([timedelta(hours=0),
                                timedelta(hours=3),
                                timedelta(hours=6),
                                timedelta(hours=9),
                                timedelta(hours=12),
                                timedelta(hours=15),
                                timedelta(hours=18),
                                timedelta(hours=21)])

        timestamps = []
        diff = end_date - start_date
        for i in range(diff.days + 1):
            daily_dates = start_date + timedelta(days=i) + img_offsets
            timestamps.extend(daily_dates.tolist())

        return timestamps

class GLDAS_Noah_v1_025Ds(MultiTemporalImageBase):
    """
    Class for reading GLDAS images in grib format.

    Parameters
    ----------
    data_path : string
        path to the grib files
    parameter : string or list, optional
        one or list of ['001', '011', '032', '051', '057', '065', '071',
                        '085_L1', '085_L2', '085_L3', '085_L4',
                        '086_L1', '086_L2', '086_L3', '086_L4',
                        '099', '111', '112', '121', '122', '131', '132', '138',
                        '155', '204', '205', '234', '235']
        parameters to read, see GLDAS documentation for more information
        Default : '086_L1'
    array_1D: boolean, optional
        if set then the data is read into 1D arrays. Needed for some legacy code.
    """

    def __init__(self, data_path, parameter='086_L1', array_1D=False):

        ioclass_kws = {'parameter': parameter,
                       'array_1D': array_1D}

        sub_path = ['%Y', '%j']
        filename_templ = "GLDAS_NOAH025SUBP_3H.A{datetime}.001.*.grb"
        super(GLDAS_Noah_v1_025Ds, self).__init__(data_path, GLDAS_Noah_v1_025Img,
                                                  fname_templ=filename_templ,
                                                  datetime_format="%Y%j.%H%M",
                                                  subpath_templ=sub_path,
                                                  exact_templ=False,
                                                  ioclass_kws=ioclass_kws)

    def tstamps_for_daterange(self, start_date, end_date):
        """
        return timestamps for daterange,

        Parameters
        ----------
        start_date: datetime
            start of date range
        end_date: datetime
            end of date range

        Returns
        -------
        timestamps : list
            list of datetime objects of each available image between
            start_date and end_date
        """
        img_offsets = np.array([timedelta(hours=0),
                                timedelta(hours=3),
                                timedelta(hours=6),
                                timedelta(hours=9),
                                timedelta(hours=12),
                                timedelta(hours=15),
                                timedelta(hours=18),
                                timedelta(hours=21)])

        timestamps = []
        diff = end_date - start_date
        for i in range(diff.days + 1):
            daily_dates = start_date + timedelta(days=i) + img_offsets
            timestamps.extend(daily_dates.tolist())

        return timestamps


class GLDASTs(GriddedNcOrthoMultiTs):

    def __init__(self, ts_path, grid_path=None):

        if grid_path is None:
            grid_path = os.path.join(ts_path, "grid.nc")

        grid = pygeogrids.netcdf.load_grid(grid_path)
        super(GLDASTs, self).__init__(ts_path, grid)
