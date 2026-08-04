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
Module for getting date lists in different intervals.
This only covers the basics like n-hourly, n-daily and dekadal.
For the generation of more complex datetime lists a package like pandas can be used.
'''

from datetime import timedelta


def daily(start, end):
    """
    Iterate over list of daily datetime objects.

    Parameters
    ----------
    start: datetime.datetime
        first date yielded
    end: datetime.datetime
        last date yielded

    Yields
    ------
    dt: datetime.datetime
        datetime object between start and end in daily steps.
    """
    for dt in n_daily(start, end, 1):
        yield dt


def hourly(start, end):
    """
    Iterate over list of hourly datetime objects.

    Parameters
    ----------
    start: datetime.datetime
        first date yielded
    end: datetime.datetime
        last date yielded

    Yields
    ------
    dt: datetime.datetime
        datetime object between start and end in daily steps.
    """
    for dt in n_hourly(start, end, 1):
        yield dt


def n_daily(start, end, n):
    """
    Iterate over list of n-daily datetime objects.

    Parameters
    ----------
    start: datetime.datetime
        first date yielded
    end: datetime.datetime
        last date yielded
    n: int
        step size

    Yields
    ------
    dt: datetime.datetime
        datetime object between start and end in daily steps.
    """
    for dt in n_hourly(start, end, n * 24):
        yield dt


def n_hourly(start, end, n):
    """
    Iterate over list of n-hourly datetime objects.

    Parameters
    ----------
    start: datetime.datetime
        first date yielded
    end: datetime.datetime
        last date yielded
    n: int
        number of hours between each yielded datetime object.

    Yields
    ------
    dt: datetime.datetime
        datetime object between start and end in n-hourly steps.
    """
    td = timedelta(hours=n)
    dt = start
    yield dt
    while True:
        dt = dt + td
        if dt > end:
            break
        yield dt
