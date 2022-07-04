"""
Module managing download of NOAH GLDAS data.
"""

import os
import sys
import glob
import argparse
from functools import partial

from trollsift.parser import validate, parse, globify
from datetime import datetime
from datedown.interface import mkdate
from datedown.dates import daily
from datedown.urlcreator import create_dt_url
from datedown.fname_creator import create_dt_fpath
from datedown.interface import download_by_dt
from datedown.down import download


def gldas_folder_get_version_first_last(
    root, fmt=None, subpaths=["{time:%Y}", "{time:%j}"]
):
    """
    Get product version and first and last product which exists under the root folder.

    Parameters
    ----------
    root: string
        Root folder on local filesystem
    fmt: string, optional
        Formatting string
        (default: "GLDAS_NOAH025_3H.A{time:%Y%m%d.%H%M}.0{version:2s}.nc4")
    subpaths: list, optional
        Format of the subdirectories under root (default: ['{:%Y}', '{:%j}']).

    Returns
    -------
    version: string
        Found product version
    start: datetime.datetime
        First found product datetime
    end: datetime.datetime
        Last found product datetime
    """
    if fmt is None:
        fmt = "GLDAS_NOAH025_3H{ep}.A{time:%Y%m%d.%H%M}.0{version:2s}.nc4"

    start = None
    end = None
    version = None
    first_folder = get_first_gldas_folder(root, subpaths)
    last_folder = get_last_gldas_folder(root, subpaths)

    if first_folder is not None:
        files = sorted(glob.glob(os.path.join(first_folder, globify(fmt))))
        data = parse(fmt, os.path.split(files[0])[1])
        start = data["time"]
        ep = data["ep"]
        version = f"GLDAS_Noah_v{data['version']}_025{data['ep']}"

    if last_folder is not None:
        files = sorted(glob.glob(os.path.join(last_folder, globify(fmt))))
        data = parse(fmt, os.path.split(files[-1])[1])
        end = data["time"]

    return version, start, end


def get_last_gldas_folder(root, subpaths):
    """
    Get last GLDAS folder name.

    Parameters
    ----------
    root : str
        Root path.
    subpaths : list of str
        Subpath information.

    Returns
    -------
    directory : str
        Last folder name.
    """
    directory = root
    for level, subpath in enumerate(subpaths):
        last_dir = get_last_formatted_dir_in_dir(directory, subpath)
        if last_dir is None:
            directory = None
            break
        directory = os.path.join(directory, last_dir)

    return directory


def get_first_gldas_folder(root, subpaths):
    """
    Get first GLDAS folder name.

    Parameters
    ----------
    root : str
        Root path.
    subpaths : list of str
        Subpath information.

    Returns
    -------
    directory : str
        First folder name.
    """
    directory = root
    for level, subpath in enumerate(subpaths):
        last_dir = get_first_formatted_dir_in_dir(directory, subpath)
        if last_dir is None:
            directory = None
            break
        directory = os.path.join(directory, last_dir)

    return directory


def get_last_formatted_dir_in_dir(folder, fmt):
    """
    Get the (alphabetically) last directory in a directory
    which can be formatted according to fmt.

    Parameters
    ----------
    folder : str
        Folder name.
    fmt : str
        Format string.

    Returns
    -------
    last_elem : str
        Last formatted directory.
    """
    last_elem = None
    root_elements = sorted(os.listdir(folder))
    for root_element in root_elements[::-1]:
        if os.path.isdir(os.path.join(folder, root_element)):
            if validate(fmt, root_element):
                last_elem = root_element
                break

    return last_elem


def get_first_formatted_dir_in_dir(folder, fmt):
    """
    Get the (alphabetically) first directory in a directory
    which can be formatted according to fmt.

    Parameters
    ----------
    folder : str
        Folder name.
    fmt : str
        Format string.

    Returns
    -------
    first_elem : str
        First formatted directory.
    """
    first_elem = None
    root_elements = sorted(os.listdir(folder))
    for root_element in root_elements:
        if os.path.isdir(os.path.join(folder, root_element)):
            if validate(fmt, root_element):
                first_elem = root_element
                break

    return first_elem


def get_gldas_start_date(product):
    """
    Get NOAH GLDAS start date.

    Parameters
    ----------
    product : str
        Product name.

    Returns
    -------
    start_date : datetime
        Start date of NOAH GLDAS product.
    """
    dt_dict = {
        "GLDAS_Noah_v20_025": datetime(1948, 1, 1, 3),
        "GLDAS_Noah_v21_025": datetime(2000, 1, 1, 3),
        "GLDAS_Noah_v21_025_EP": datetime(2000, 1, 1, 3),
    }

    return dt_dict[product]


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
        description="Download GLDAS data.",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "localroot",
        help="Root of local filesystem where" "the data is stored.",
    )

    parser.add_argument(
        "-s",
        "--start",
        type=mkdate,
        help=(
            "Startdate as YYYY-MM-DD. "
            "If not given then the target"
            "folder is scanned for a start date. If no data"
            "is found there then the first available date "
            "of the product is used."
        ),
    )

    parser.add_argument(
        "-e",
        "--end",
        type=mkdate,
        help=(
            "Enddate. In format YYYY-MM-DD.If not given then the "
            "current date is used."
        ),
    )

    help_string = "\n".join(
        [
            "GLDAS product to download.",
            "GLDAS_Noah_v20_025 available from {} to 2014-12-31",
            "GLDAS_Noah_v21_025 available from {}",
            "GLDAS_Noah_v21_025_EP available after GLDAS_Noah_v21_025",
        ]
    )

    help_string = help_string.format(
        get_gldas_start_date("GLDAS_Noah_v20_025"),
        get_gldas_start_date("GLDAS_Noah_v21_025"),
    )

    parser.add_argument(
        "--product",
        choices=[
            "GLDAS_Noah_v20_025",
            "GLDAS_Noah_v21_025",
            "GLDAS_Noah_v21_025_EP",
        ],
        default="GLDAS_Noah_v21_025",
        help=help_string,
    )

    parser.add_argument("--username", help="Username to use for download.")

    parser.add_argument("--password", help="password to use for download.")

    parser.add_argument(
        "--n_proc",
        default=1,
        type=int,
        help="Number of parallel processes to use for" "downloading.",
    )

    args = parser.parse_args(args)
    # set defaults that can not be handled by argparse

    # Compare versions to prevent mixing data sets
    version, first, last = gldas_folder_get_version_first_last(args.localroot)
    if args.product and version and (args.product != version):
        raise Exception(
            "Error: Found products of different version ({}) "
            "in {}. Abort download!".format(version, args.localroot)
        )

    if args.start is None or args.end is None:
        if not args.product:
            args.product = version
        if args.start is None:
            if last is None:
                if args.product:
                    args.start = get_gldas_start_date(args.product)
                else:
                    # In case of no indication if version, use GLDAS Noah 2.0
                    # start time, because it has the longest time span
                    args.start = get_gldas_start_date("GLDAS_Noah_v20_025")
            else:
                args.start = last
        if args.end is None:
            args.end = datetime.now()

    prod_urls = {
        "GLDAS_Noah_v20_025": {
            "root": "hydro1.gesdisc.eosdis.nasa.gov",
            "dirs": ["data", "GLDAS", "GLDAS_NOAH025_3H.2.0", "%Y", "%j"],
        },
        "GLDAS_Noah_v21_025": {
            "root": "hydro1.gesdisc.eosdis.nasa.gov",
            "dirs": ["data", "GLDAS", "GLDAS_NOAH025_3H.2.1", "%Y", "%j"],
        },
        "GLDAS_Noah_v21_025_EP": {
            "root": "hydro1.gesdisc.eosdis.nasa.gov",
            "dirs": ["data", "GLDAS", "GLDAS_NOAH025_3H_EP.2.1", "%Y", "%j"],
        },
    }

    args.urlroot = prod_urls[args.product]["root"]
    args.urlsubdirs = prod_urls[args.product]["dirs"]
    args.localsubdirs = ["%Y", "%j"]

    print(
        "Downloading data from {} to {} "
        "into folder {}.".format(
            args.start.isoformat(), args.end.isoformat(), args.localroot
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

    dts = list(daily(args.start, args.end))
    url_create_fn = partial(
        create_dt_url, root=args.urlroot, fname="", subdirs=args.urlsubdirs
    )
    fname_create_fn = partial(
        create_dt_fpath,
        root=args.localroot,
        fname="",
        subdirs=args.localsubdirs,
    )

    down_func = partial(
        download,
        num_proc=args.n_proc,
        username=args.username,
        password="'" + args.password + "'",
        recursive=True,
        filetypes=["nc4", "nc4.xml"],
    )
    download_by_dt(
        dts, url_create_fn, fname_create_fn, down_func, recursive=True
    )


def run():
    main(sys.argv[1:])
