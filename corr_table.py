#!/usr/bin/env python3

import os
import json

from astropy.io import fits

DATA_DIR = '/home/nobus/develop/vsminer/data'
JOB = '3757403'
JOB_DIR = os.path.join('/home/nobus/develop/vsminer/data', JOB)

"""
from astroquery.simbad import Simbad
import astropy.coordinates as coord
import astropy.units as u

result_table = Simbad.query_region(coord.SkyCoord(ra=25.914404945336344, dec=50.687094460689295, unit=(u.deg, u.deg)), radius=0.05 * u.deg)

sss = result_table[0][0].decode('ascii')
>>> sss.replace(' ', '+')
'*+phi+Per'

https://www.aavso.org/vsx/index.php?ident=*+phi+Per&view=api.object&format=json
{"VSXObject":{"Name":"phi Per","AUID":"000-BBD-264","RA2000":"25.91517","Declination2000":"50.68872","ProperMotionRA":"24.5900","ProperMotionDec":"-14.0100","VariabilityType":"GCAS","Period":"19.5","MaxMag":"3.96 V","MinMag":"4.11 V","SpectralType":"B2Vne+B3Vne","Category":"Variable","OID":"26210","Constellation":"Per"}}

"""


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
