"""
Download latest GLDASv1 and GLDASv2.

@author: Plocon Andreea
created on: 15.05.2014
"""
import os
import ftplib

from datetime import datetime


def download(host, server_path, raw, download_path, files_per_day=16):
    """
    Download latest GLDAS from ftp server.

    Parameters
    ----------
    host : str
        Host name
    server_path : str
        Path to data on server.
    raw : str
        Path to data local.
    download_path : str
        Path where to save the downloaded files.
    files_per_day: int
        Optional, number of files in one day. For GLDAS = 16.
    """

    last = get_last_year_day(raw)

    last_year, last_day = last.split('_')
    log_file = os.path.join(download_path, 'download_log.txt')
    downloads = 0
    status = 'ok'

    # connect to server
    ftp = ftplib.FTP(host, 'anonymous')
    # change directory on server
    ftp.cwd(server_path)

    years = []
    ftp.retrlines('NLST', years.append)

    for year in sorted(years):
        try:
            int(year)
        except ValueError:
            continue
        else:
            if int(year) >= int(last_year):
                ftp.cwd(year)
                days = []
                ftp.retrlines('NLST', days.append)
                for day in sorted(days):
                    if int(day) > int(last_day):
                        with open(log_file, 'a') as f:
                            f.write('%s -> Downloading year: %s day:%s \n' %
                                    (str(datetime.now()), year, day))
                        day_downloads = 0
                        ftp.cwd(day)
                        files2download = []
                        ftp.retrlines('NLST', files2download.append)

                        # create local directories
                        year_dir = os.path.join(download_path, year)
                        if not os.path.exists(year_dir):
                            os.makedirs(year_dir)
                        day_dir = os.path.join(year_dir, day)
                        if not os.path.exists(day_dir):
                            os.makedirs(day_dir)

                        # download files
                        for filename in files2download:
                            downloads += 1
                            day_downloads += 1
                            ftp.sendcmd("TYPE i")
                            size_before = ftp.size(filename)

                            local_filename = os.path.join(day_dir, filename)
                            local_file = open(local_filename, 'wb')
                            ftp.retrbinary(
                                'RETR ' + filename, local_file.write)
                            local_file.close()

                            size_after = os.path.getsize(local_filename)

                            # check downloaded file
                            if size_before != size_after:
                                status = 'wrong'
                                with open(log_file, 'a') as f:
                                    f.write('%s -> WARNING: check file %s \n'
                                            % (str(datetime.now()), local_filename))

                        # check if day is complete
                        if day_downloads != files_per_day:
                            status = 'wrong'
                            with open(log_file, 'a') as f:
                                f.write('%s -> WARNING: check day %s \n'
                                        % (str(datetime.now()), day))

                        # return to year directory
                        ftp.cwd(os.path.join(server_path, year))

                # return to path directory
                ftp.cwd(server_path)

    ftp.quit()

    with open(log_file, 'a') as f:
        f.write('%s -> DOWNLOADED %d FILES ' %
                (str(datetime.now()), downloads))
        if status == 'ok':
            f.write('NO WARNINGS!')
        else:
            f.write('CHECK WARNINGS!')
        f.write('\n--------------------------\n')


def get_last_year_day(raw_path):
    """
    Get last year and day in the raw data.

    Parameters
    ----------
    raw_path : str
        Path to raw data local.

    Returns
    -------
    year_day: str
        String containing last year and last_day
    """

    last_year = '0'
    last_day = '0'

    for year in os.walk(raw_path).next()[1]:
        try:
            int(year)
        except ValueError:
            continue
        else:
            if int(year) > int(last_year):
                last_year = year

    if last_year != '0':
        for day in os.walk(os.path.join(raw_path, last_year)).next()[1]:
            try:
                int(day)
            except ValueError:
                continue
            else:
                if int(day) > int(last_day):
                    last_day = day

    return last_year + '_' + last_day


if __name__ == '__main__':

    # download GLDASv1_025
    host = 'hydro1.sci.gsfc.nasa.gov'
    server_path = '/data/s4pa/GLDAS_V1/GLDAS_NOAH025SUBP_3H'

    raw = '.../raw_GLDAS/'
    download_path = '.../raw_GLDAS/'

    download(host, server_path, raw, download_path, files_per_day=16)
