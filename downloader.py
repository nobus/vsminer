#!/usr/bin/env python3

import os
import shutil

from astropy.utils.data import download_file


CACHE=False

DATA_DIR = '/home/nobus/develop/vsminer/data'
JOB = '3757403'
JOB_DIR = os.path.join('/home/nobus/develop/vsminer/data', JOB)


def _downloader(pref):
    """
        new_fits
        rdls
        axy
        corr
    """
    astrometry = 'http://nova.astrometry.net'

    url_fits = f'{astrometry}/{pref}_file/{JOB}'

    fits_file = download_file(url_fits, cache=CACHE)

    shutil.copy2(fits_file, JOB_DIR)

    old_file_name = os.path.join(
        JOB_DIR,
        os.path.join(
            JOB_DIR, 
            os.path.split(fits_file)[-1]
            )
        )

    new_file_name = os.path.join(JOB_DIR, f'{pref}.fits')

    shutil.move(old_file_name, new_file_name)


def main():
    if not os.path.exists(JOB_DIR):
        os.mkdir(JOB_DIR)

    _downloader('new_fits')
    _downloader('rdls')
    _downloader('axy')
    _downloader('corr')


if __name__ == '__main__':
    main()
