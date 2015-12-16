import warnings
import numpy as np

try:
    import pygrib
except ImportError:
    warnings.warn("pygrib has not been imported")

import rs_data_readers.dataset_base as dsbase

from datetime import timedelta

from rs_data_readers.GLDAS_NOAH.grid import GLDAS025Cellgrid


class GLDAS025Img(dsbase.DatasetImgBase):
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
    """

    def __init__(self, data_path, parameter='086_L1'):

        grid = GLDAS025Cellgrid()

        self.fill_values = np.repeat(9999., 1440 * 120)
        if type(parameter) != list:
            parameter = [parameter]
        self.parameters = parameter

        sub_path = ['%Y', '%j']
        filename_templ = "GLDAS_NOAH025SUBP_3H.A%Y%j.%H%M.001.*.grb"
        super(GLDAS025Img, self).__init__(data_path,
                                          filename_templ=filename_templ,
                                          sub_path=sub_path,
                                          exact_templ=False,
                                          grid=grid)

    def _read_spec_file(self, filename, timestamp=None):

        return_img = {}
        layers = {'085': 1, '086': 1}

        try:
            grbs = pygrib.open(filename)
        except IOError as e:
            print e
            print " ".join([filename, "can not be opened"])
            raise e

        ids = []
        for parameter in self.parameters:
            ids.append(int(parameter.split('_')[0]))
        parameter_ids = np.unique(np.array(ids))

        for message in grbs:
            if message['indicatorOfParameter'] in parameter_ids:
                parameter_id = '{:03d}'.format(message['indicatorOfParameter'])

                if parameter_id in layers.keys():
                    parameter = '_'.join((parameter_id, 'L' +
                                          str(layers[parameter_id])))

                    if parameter in self.parameters:
                        param_data = np.concatenate((
                            self.fill_values,
                            np.ma.getdata(message['values']).flatten()))
                        return_img[parameter] = param_data[self.grid.activegpis]
                    layers[parameter_id] += 1

                else:
                    parameter = parameter_id
                    param_data = np.concatenate((
                        self.fill_values,
                        np.ma.getdata(message['values']).flatten()))
                    return_img[parameter] = param_data[self.grid.activegpis]

        grbs.close()
        for parameter in self.parameters:
            try:
                return_img[parameter]
            except KeyError:
                print filename[filename.rfind('GLDAS'):], \
                    'corrupt file - filling image with nan values'
                return_img[parameter] = np.empty(self.grid.n_gpi)
                return_img[parameter].fill(np.nan)

        return (return_img, {}, timestamp, self.grid.activearrlon,
                self.grid.activearrlat, None)

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
        for i in xrange(diff.days + 1):
            daily_dates = start_date + timedelta(days=i) + img_offsets
            timestamps.extend(daily_dates.tolist())

        return timestamps
