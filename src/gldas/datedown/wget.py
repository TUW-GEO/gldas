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
Interface to wget command line utility.
'''

import subprocess
import os


def download(url, target, username=None, password=None, cookie_file=None,
             recursive=False, filetypes=None):
    """
    Download a url using wget.
    Retry as often as necessary and store cookies if
    authentification is necessary.

    Parameters
    ----------
    url: string
        URL to download
    target: string
        path on local filesystem where to store the downloaded file
    username: string, optional
        username
    password: string, optional
        password
    cookie_file: string, optional
        file where to store cookies
    recursive: boolean, optional
        If set then no exact filenames can be given.
        The data will then be downloaded recursively and stored in the target folder.
    filetypes: list, optional
        list of file extension to download, any others will no be downloaded
    """
    cmd_list = ['wget',
                url,
                '--retry-connrefused']

    if recursive:
        cmd_list = cmd_list + ['-P', target]
        cmd_list = cmd_list + ['-nd']
        cmd_list = cmd_list + ['-np']
        cmd_list = cmd_list + ['-r']
    else:
        cmd_list = cmd_list + ['-O', target]

    if filetypes is not None:
        cmd_list = cmd_list + ['-A ' + ','.join(filetypes)]

    target_path = os.path.split(target)[0]
    if not os.path.exists(target_path):
        os.makedirs(target_path)

    if username is not None:
        cmd_list.append('--user={}'.format(username))
    if password is not None:
        cmd_list.append('--password={}'.format(password))
    if cookie_file is not None:
        cmd_list = cmd_list + [
            '--load-cookies', cookie_file,
            '--save-cookies', cookie_file,
            '--keep-session-cookies']

    subprocess.call(" ".join(cmd_list), shell=True)


def map_download(url_target, username=None, password=None, cookie_file=None,
                 recursive=False, filetypes=None):
    """
    variant of the function that only takes one argument.
    Otherwise map_async of the multiprocessing module can not work with the function.

    Parameters
    ----------
    url_target: list
        first element the url, second the target string
    username: string, optional
        username
    password: string, optional
        password
    cookie_file: string, optional
        file where to store cookies
    recursive: boolean, optional
        If set then no exact filenames can be given.
        The data will then be downloaded recursively and stored in the target folder.
    filetypes: list, optional
        list of file extension to download, any others will no be downloaded
    """
    download(url_target[0], url_target[1],
             username=username,
             password=password,
             cookie_file=cookie_file,
             recursive=recursive,
             filetypes=filetypes)
