#!/usr/bin/env python3

import os
import sys
import shutil

import msgpack
import msgpack_numpy as m
m.patch()

import matplotlib
import matplotlib.pyplot as plt

from astropy.io import fits
from astropy.utils.data import download_file


CACHE=True

DATA_DIR = '/home/nobus/develop/vsminer/data'
JOB = '3757403'
JOB_DIR = os.path.join('/home/nobus/develop/vsminer/data', JOB)


def downloader(pref):
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

    return new_file_name


def image_converter(fpath):
    hdu_list = fits.open(fpath)

    if hdu_list:
        image_data = hdu_list[0].data

        matplotlib.image.imsave(
            os.path.join(JOB_DIR, 'new_fits.png'),
            image_data,
            cmap='gray',
            vmin=2.5e3,
            vmax=3.6e3)

        image_data_enc = msgpack.packb(image_data, default=m.encode)

        fd = open(os.path.join(JOB_DIR, 'new_fits.mpack'), 'wb')
        fd.write(image_data_enc)
        fd.close()
    else:
        print('No image data', file=sys.stderr)

    hdu_list.close()

def main():
    if not os.path.exists(JOB_DIR):
        os.mkdir(JOB_DIR)

    downloader('rdls')
    downloader('axy')
    downloader('corr')

    new_fits_fpath = downloader('new_fits')
    image_converter(new_fits_fpath)


if __name__ == '__main__':
    main()
