# The MIT License (MIT)
#
# Copyright (c) 2022, Christoph Paulik
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

'''
Interface for the package.
'''

from datetime import datetime
from gldas.datedown.down import check_downloaded
from gldas.datedown.dates import n_hourly
from gldas.datedown.urlcreator import create_dt_url
from gldas.datedown.fname_creator import create_dt_fpath
from gldas.datedown.down import download
import warnings
from functools import partial
import sys
import argparse


def download_by_dt(dts, url_create_fn,
                   fpath_create_fn, download_fn,
                   passes=3, recursive=False):
    """
    Download data for datetimes. If files are missing try
    again passes times.

    Parameters
    ----------
    dts: list
        list of datetime.datetime objects
    url_create_fn: function
        function that creates an URL from a datetime object
    fpath_create_fn: function
        function that creates a filename from a datetime object
    download_fn: function
        function that transfers data from a list
        of URLs to a list of filenames.
        Takes two arguments (url_list, fname_list)
    passes: int, optional
        if files are missing then try again passes times
    recursive: boolean, optional
        If set then no exact filenames can be given.
        The data will then be downloaded recursively and stored in the target folder.
        No checking of downloaded files is possible in this case.
    """
    urls = map(url_create_fn, dts)
    fnames = map(fpath_create_fn, dts)
    for p in range(passes):
        download_fn(urls, fnames)
        if not recursive:
            no_urls, no_fnames = check_downloaded(urls, fnames)
            urls = no_urls
            fnames = no_fnames
            if len(no_urls) == 0:
                break
        else:
            urls = []
            break

    if len(urls) != 0:
        warnings.warn("Not all URL's were downloaded.")
        warnings.warn("\n".join(urls))


def mkdate(datestring):
    if len(datestring) == 10:
        return datetime.strptime(datestring, '%Y-%m-%d')
    if len(datestring) == 16:
        return datetime.strptime(datestring, '%Y-%m-%dT%H:%M')


def n_hours(intervalstring):
    """
    Convert an interval string like 1D, 6H etc. to the
    number of hours it represents.
    """
    multid = {'H': 1,
              'D': 24}
    multi = multid[intervalstring[-1].upper()]
    hours = multi * int(intervalstring[:-1])
    return hours


def parse_args(args):
    """
    Parse command line parameters

    :param args: command line parameters as list of strings
    :return: command line parameters as :obj:`argparse.Namespace`
    """
    parser = argparse.ArgumentParser(
        description="Download data in parallel using wget. Based on datetimes.")
    parser.add_argument("start", type=mkdate,
                        help="Startdate. Either in format YYYY-MM-DD or YYYY-MM-DDTHH:MM.")
    parser.add_argument("end", type=mkdate,
                        help="Enddate. Either in format YYYY-MM-DD or YYYY-MM-DDTHH:MM.")
    parser.add_argument("urlroot",
                        help='Root of URL of the remote dataset.')
    parser.add_argument("urlfname",
                        help='Filenames of the remote dataset.')
    parser.add_argument("localroot",
                        help='Root of local filesystem.')
    parser.add_argument("--urlsubdirs", nargs='+',
                        help=('Subdirectories to put between urlroot and urlfname.'
                              'This can be a list of directories that can contain date string templates.'
                              'e.g. --urlsubdirs %%Y %%m would look for files in urlroot/YYYY/MM/urlfname.'))
    parser.add_argument("--localfname",
                        help=('Filenames of the local dataset. '
                              'If not given the filenames of the remote dataset are used.'))
    parser.add_argument("--localsubdirs", nargs='+',
                        help=('Subdirectories to put between localroot and localfname.'
                              'This can be a list of directories that can contain date string templates.'
                              'e.g. --localsubdirs %%Y %%m would look for files in localroot/YYYY/MM/localfname.'
                              'If not given then the urlsubdirs are used.'))
    parser.add_argument("--interval", type=n_hours, default='1D',
                        help=('Interval of datetimes between the start and end. '
                              'Supported types are e.g. 6H for 6 hourly or 2D for 2 daily.'))
    parser.add_argument("--username",
                        help='Username to use for download.')
    parser.add_argument("--password",
                        help='password to use for download.')
    parser.add_argument("--n_proc", default=1, type=int,
                        help='Number of parallel processes to use for downloading.')
    args = parser.parse_args(args)
    # set defaults that can not be handled by argparse
    if args.localfname is None:
        args.localfname = args.urlfname
    if args.localsubdirs is None:
        args.localsubdirs = args.urlsubdirs
    return args


def main(args):
    args = parse_args(args)

    dts = list(n_hourly(args.start, args.end, args.interval))
    url_create_fn = partial(create_dt_url, root=args.urlroot,
                            fname=args.urlfname, subdirs=args.urlsubdirs)
    fname_create_fn = partial(create_dt_fpath, root=args.localroot,
                              fname=args.localfname, subdirs=args.localsubdirs)
    down_func = partial(download,
                        num_proc=args.n_proc,
                        username=args.username,
                        password=args.password)
    download_by_dt(dts, url_create_fn,
                   fname_create_fn, down_func)


def run():
    main(sys.argv[1:])


def parse_args_recursive(args):
    """
    Parse command line parameters for recursive download

    :param args: command line parameters as list of strings
    :return: command line parameters as :obj:`argparse.Namespace`
    """
    parser = argparse.ArgumentParser(
        description="Download data recursively in parallel using wget. Based on datetimes.")
    parser.add_argument("start", type=mkdate,
                        help="Startdate. Either in format YYYY-MM-DD or YYYY-MM-DDTHH:MM.")
    parser.add_argument("end", type=mkdate,
                        help="Enddate. Either in format YYYY-MM-DD or YYYY-MM-DDTHH:MM.")
    parser.add_argument("urlroot",
                        help='Root of URL of the remote dataset.')
    parser.add_argument("localroot",
                        help='Root of local filesystem.')
    parser.add_argument("--urlsubdirs", nargs='+',
                        help=('Subdirectories to put between urlroot and urlfname.'
                              'This can be a list of directories that can contain date string templates.'
                              'e.g. --urlsubdirs %%Y %%m would look for files in urlroot/YYYY/MM/urlfname.'))
    parser.add_argument("--localsubdirs", nargs='+',
                        help=('Subdirectories to put between localroot and localfname.'
                              'This can be a list of directories that can contain date string templates.'
                              'e.g. --localsubdirs %%Y %%m would look for files in localroot/YYYY/MM/localfname.'
                              'If not given then the urlsubdirs are used.'))
    parser.add_argument("--interval", type=n_hours, default='1D',
                        help=('Interval of datetimes between the start and end. '
                              'Supported types are e.g. 6H for 6 hourly or 2D for 2 daily.'))
    parser.add_argument("--username",
                        help='Username to use for download.')
    parser.add_argument("--password",
                        help='password to use for download.')
    parser.add_argument("--n_proc", default=1, type=int,
                        help='Number of parallel processes to use for downloading.')
    args = parser.parse_args(args)
    # set defaults that can not be handled by argparse
    if args.localsubdirs is None:
        args.localsubdirs = args.urlsubdirs
    return args


def main_recursive(args):
    args = parse_args_recursive(args)

    dts = list(n_hourly(args.start, args.end, args.interval))
    url_create_fn = partial(create_dt_url, root=args.urlroot,
                            fname='', subdirs=args.urlsubdirs)
    fname_create_fn = partial(create_dt_fpath, root=args.localroot,
                              fname='', subdirs=args.localsubdirs)
    down_func = partial(download,
                        num_proc=args.n_proc,
                        username=args.username,
                        password=args.password,
                        recursive=True)
    download_by_dt(dts, url_create_fn,
                   fname_create_fn, down_func,
                   recursive=True)


def run_recursive():
    main_recursive(sys.argv[1:])
