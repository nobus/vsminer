#!/usr/bin/env python3

import os
import sys
import time
import json
import requests

from random import randint
from optparse import OptionParser

from astropy.io import fits
import astropy.coordinates as coord
import astropy.units as u

from astroquery.simbad import Simbad

DATA_DIR = '/home/nobus/develop/vsminer/data'
#JOB = '3757403'
#JOB_DIR = os.path.join('/home/nobus/develop/vsminer/data', JOB)


def get_info_from_simbad(ra, dec):
    while True:
        time.sleep(randint(3, 9))

        try:
            result_table = Simbad.query_region(
                coord.SkyCoord(ra=ra, dec=dec, unit=(u.deg, u.deg)),
                radius=0.05 * u.deg)

            obj_name = result_table[0][0].decode('ascii')

            return obj_name
        except Exception as ex:
            print('Simbad: ', ex, file=sys.stderr)


def get_info_from_aavso(ra, dec):
    obj_name = get_info_from_simbad(ra, dec)

    aavso_format = obj_name.replace(' ', '+')
    aavso_format = aavso_format.lstrip('V*')

    print(f'Get AAVSO data for {aavso_format}', file=sys.stderr)

    while True:
        time.sleep(randint(3, 9))

        try:
            resp = requests.get(f'https://www.aavso.org/vsx/index.php?ident={aavso_format}&view=api.object&format=json')

            """
            {"VSXObject": {
                "Name":"phi Per",
                "AUID":"000-BBD-264",
                "RA2000":"25.91517",
                "Declination2000":"50.68872",
                "ProperMotionRA":"24.5900",
                "ProperMotionDec":"-14.0100",
                "VariabilityType":"GCAS",
                "Period":"19.5",
                "MaxMag":"3.96 V",
                "MinMag":"4.11 V",
                "SpectralType":"B2Vne+B3Vne",
                "Category":"Variable",
                "OID":"26210",
                "Constellation":"Per"
                }
            }
            """
            aavso_data = json.loads(resp.text)

            print(aavso_data, file=sys.stderr)

            return {'name': obj_name, 'aavso': aavso_data.get('VSXObject', {})}
        except Exception as ex:
            print('AAVSO: ', ex, file=sys.stderr)


def main():
    parser = OptionParser()
    parser.add_option('-j', '--job', type='str', dest='job_num')

    (options, args) = parser.parse_args()
    job_num = options.job_num
    job_dir = os.path.join(DATA_DIR, job_num)

    hdu = fits.open(f'{job_dir}/corr.fits', mode='readonly', ignore_missing_end=True)
    fdata = hdu[1].data
    cols = hdu[1].columns
    hdu.close()

    corr_data = []
    aavso_data = []

    for row in fdata:
        data = [float(e) for e in row]
        corr_data.append(data)
        aavso_data.append(get_info_from_aavso(data[2], data[3]))

    result = {
        'cols': cols.names,
        'corr_data': corr_data,
        'aavso_data': aavso_data,
    }

    print(json.dumps(result))


if __name__ == '__main__':
    main()
