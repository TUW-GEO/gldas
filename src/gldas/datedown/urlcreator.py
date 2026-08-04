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
Module for creating the URLs from the datetimes.
'''


def create_dt_url(dt, root, fname, subdirs=[]):
    """
    Create URLs from root + fname and a list of subdirectories.
    fname and subdirs will be put through dt.strftime.

    Parameters
    ----------
    dt: datetime.datetime
        date as basis for the URL
    root: string
        root of the url
    fname: string
        filename to use
    subdirs: list, optional
        list of strings.
        Each element represents a subdirectory.
        For example the list ['%Y', '%m'] would lead to a URL of
        ``root/YYYY/MM/fname`` or for a dt of datetime(2000,12,31)
        ``root/2000/12/fname``

    Returns
    -------
    url: string
    """
    dt_subdirs = []
    for subdir in subdirs:
        dt_subdirs.append(dt.strftime(subdir))
    dt_fname = dt.strftime(fname)
    url = '/'.join([root] + dt_subdirs + [dt_fname])
    return url
