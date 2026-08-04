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
Module that puts the things toghether.
'''

from multiprocessing import Pool
import tempfile
import os
from functools import partial

import gldas.datedown.wget as wget


def download(urls, targets, num_proc=1, username=None, password=None,
             recursive=False, filetypes=None):
    """
    Download the urls and store them at the target filenames.

    Parameters
    ----------
    urls: iterable
        iterable over url strings
    targets: iterable
        paths where to store the files
    num_proc: int, optional
        Number of parallel downloads to start
    username: string, optional
        Username to use for login
    password: string, optional
        Password to use for login
    recursive: boolean, optional
        If set then no exact filenames can be given.
        The data will then be downloaded recursively and stored in the target folder.
    filetypes: list, optional
        list of file extension to download, any others will no be downloaded
    """
    p = Pool(num_proc)
    # partial function for Pool.map
    cookie_file = tempfile.NamedTemporaryFile()
    dlfunc = partial(wget.map_download,
                     username=username,
                     password=password,
                     cookie_file=cookie_file.name,
                     recursive=recursive,
                     filetypes=filetypes)

    p.map_async(dlfunc, zip(urls, targets)).get(9999999)
    cookie_file.close()


def check_downloaded(urls, targets):
    """
    Check if files that should be downloaded exist.
    If not then return a list of not downloaded URLs.

    Parameters
    ----------
    urls: iterable
        iterable over url strings
    targets: iterable
        paths where to store the files

    Returns
    -------
    not_urls: list
        list of urls that do not exist locally
    not_fnames: list
        list of filenames that do not exist locally
    """
    not_urls = []
    not_fnames = []
    for url, target in zip(urls, targets):
        if not os.path.exists(target):
            not_urls.append(url)
            not_fnames.append(target)

    return not_urls, not_fnames
