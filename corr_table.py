#!/usr/bin/env python3

import os
import json

from astropy.io import fits

DATA_DIR = '/home/nobus/develop/vsminer/data'
JOB = '3757403'
JOB_DIR = os.path.join('/home/nobus/develop/vsminer/data', JOB)


def main():
    hdu = fits.open(f'{JOB_DIR}/corr.fits', mode='readonly', ignore_missing_end=True)
    fdata = hdu[1].data
    cols = hdu[1].columns
    hdu.close()

    data = []

    for row in fdata:
        data.append([float(e) for e in row])

    result = {
        'cols': cols.names,
        'data': data
    }

    print(json.dumps(result))


if __name__ == '__main__':
    main()