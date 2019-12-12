# -*- coding: utf-8 -*-

import re
import os
import sys
import json
import time
import requests

import shutil

import numpy as np
import msgpack
import msgpack_numpy as m
m.patch()

import matplotlib
import matplotlib.pyplot as plt

from random import randint
from datetime import datetime

import astropy.coordinates as coord
import astropy.units as u
from astropy.io import fits
from astropy.utils.data import download_file

from astroquery.simbad import Simbad

from django.conf import settings
from django.core.management.base import BaseCommand

from vs_app.models import AstroMetryJob, CorrFits, NewFits, SimbadData, AAVSOData


class ProtoLoader:
    def __init__(self, logger, job_number, sleep_interval=(3, 9)):
        self.logger = logger
        self.job_number = job_number
        self.sleep_interval = sleep_interval

        self.radius = 0.05

    def rsleep(self):
        time.sleep(randint(*self.sleep_interval))

    def run(self):
        raise(NotImplementedError)


class AstrometryLoader(ProtoLoader):
    def __init__(
            self,
            logger,
            job_number,
            status_url,
            job_info=False, 
            new_image=False, 
            corr_image=False, 
            all_data=True
        ):

        super().__init__(logger, job_number)

        self.status_url = status_url
        self.job_info = job_info
        self.new_image = new_image
        self.corr_image = corr_image
        self.all_data = all_data

        self.astrometry_url = 'http://nova.astrometry.net'
        self.job_dir = os.path.join(settings.MEDIA_ROOT, str(self.job_number))

    def get_job_info(self):
        """
        http://astrometry.net/doc/net/api.html#getting-job-results
        """

        self.logger(f'Get job info for job={self.job_number}')
        resp = requests.get(f'{self.astrometry_url}/api/jobs/{self.job_number}/info/')

        job_info = json.loads(resp.text)
        job_stat = job_info.get('status', '')

        if job_stat == 'success':
            calibration = job_info.get('calibration', {})

            obj, created = AstroMetryJob.objects.get_or_create(
                job_number=self.job_number,
                center_ra=calibration['ra'],
                center_dec=calibration['dec'],
            )

            obj.orientation = calibration.get('orientation', None)
            obj.pixscale = calibration.get('pixscale', None)
            obj.radius = calibration.get('radius', None)
            obj.url = self.status_url

            if not created:
                obj.center_ra = calibration['ra']
                obj.center_dec = calibration['dec']

            obj.save()
        else:
            raise BaseException(f'Job {self.job_id} has wrong status: {job_stat}')

    def _download_file(self, pref):
        url_fits = f'{self.astrometry_url}/{pref}_file/{self.job_number}'

        fits_file = download_file(url_fits, cache=False)

        shutil.copy2(fits_file, self.job_dir)

        old_file_path = os.path.join(
            self.job_dir,
            os.path.join(
                self.job_dir,
                os.path.split(fits_file)[-1]
                )
            )

        new_file_path = os.path.join(self.job_dir, f'{pref}.fits')
        shutil.move(old_file_path, new_file_path)

        return new_file_path

    def minmax_calc(self, image_data):
        # magic numbers
        NBINS = 1000
        K = 1000

        vmin = None
        vmax = None
        prev_elem = 0

        h = np.histogram(image_data.flatten(), bins=NBINS)

        for count, elem in enumerate(h[0]):
            if elem > K:
                vmax = count

                if prev_elem < K:
                    vmin = count

            prev_elem = elem

        return h[1][vmin], h[1][vmax]

    def set_headers(self, hdu_list):
        params = {}

        to_int = lambda x: int(x)
        key_map = {
            'NAXIS': ['naxis', to_int],
            'NAXIS1': ['naxis1', to_int],
            'NAXIS2': ['naxis2', to_int],
            'DATE-OBS': ['date_obs', lambda x: datetime.strptime(x, '%d/%m/%Y').date()],
            'UT-START': ['ut_start', lambda x: datetime.strptime(x, '%H:%M:%S').time()],
            'EXPTIME': ['exptime', to_int],
            'CRVAL1': ['ref_point_ra', to_int],
            'CRVAL2': ['ref_point_dec', to_int],
            'CRPIX1': ['ref_point_x', to_int],
            'CRPIX2': ['ref_point_y', to_int],
            'CD1_1': ['tranform_matrix', to_int],
            'SCALE': ['scale', to_int],
        }

        for elem in hdu_list[0].header:
            if elem in key_map:
                params[key_map[elem][0]] = key_map[elem][1](hdu_list[0].header[elem])

        job_obj = AstroMetryJob.objects.get(job_number=self.job_number)
        NewFits.objects.filter(astro_job=job_obj).delete()

        params['astro_job'] = job_obj
        NewFits(**params).save()

    def get_new_image(self):
        fits_fpath = self._download_file('new_fits')
        hdu_list = fits.open(fits_fpath)

        if hdu_list:
            self.set_headers(hdu_list)

            image_data = hdu_list[0].data
            vmin, vmax = self.minmax_calc(image_data)

            matplotlib.image.imsave(
                os.path.join(self.job_dir, 'new_fits.png'),
                image_data,
                cmap='gray',
                vmin=vmin,
                vmax=vmax)

            image_data_enc = msgpack.packb(image_data, default=m.encode)

            fd = open(os.path.join(self.job_dir, 'new_fits.mpack'), 'wb')
            fd.write(image_data_enc)
            fd.close()
        else:
            self.logger('No image data')

        hdu_list.close()

    def get_corr(self):
        fits_fpath = self._download_file('corr')

        hdu_list = fits.open(fits_fpath)
        fdata = hdu_list[1].data
        cols = hdu_list[1].columns
        hdu_list.close()

        corr_data = []

        job_obj = AstroMetryJob.objects.get(job_number=self.job_number)
        CorrFits.objects.filter(astro_job=job_obj).delete()

        for row in fdata:
            data = [float(e) for e in row]
            obj_params = dict(zip(cols.names, data))
            obj_params['astro_job'] = job_obj

            corr_obj = CorrFits(**obj_params)
            corr_obj.save()

    def get_all(self):
        self.get_job_info()
        self.get_new_image()
        self.get_corr()

    def run(self):
        if not os.path.exists(self.job_dir):
            os.mkdir(self.job_dir)

        if self.all_data:
            self.get_all()
        else:
            if self.job_info:
                self.get_job_info()

            if self.new_image:
                self.get_new_image()

            if self.corr_image:
                self.get_corr()

class SimbadLoader(ProtoLoader):
    def _get_info_from_simbad(self, ra, dec):
        """
        MAIN_ID        RA           DEC      RA_PREC DEC_PREC COO_ERR_MAJA COO_ERR_MINA COO_ERR_ANGLE COO_QUAL COO_WAVELENGTH     COO_BIBCODE    
             "h:m:s"       "d:m:s"                         mas          mas           deg                                                 
        --------- ------------- ------------- ------- -------- ------------ ------------ ------------- -------- -------------- -------------------
        * phi Per 01 43 39.6379 +50 41 19.432      11       11        0.110        0.120            90        A              O 2007A&A...474..653V
        """
        def _coord_convert(ra_hms, dec_dms):
            # '01 43 39.6379', '+50 41 19.432' => 25.915157916666665, 50.68873111111111
            c = coord.SkyCoord(ra_hms, dec_dms, unit=(u.hourangle, u.deg))
            return c.ra.value, c.dec.value

        ret = {}

        while True:
            self.rsleep()

            try:
                result_table = Simbad.query_region(
                    coord.SkyCoord(ra=ra, dec=dec, unit=(u.deg, u.deg)),
                    radius=self.radius*u.deg)

                data = result_table[0]

                ret['MAIN_ID'] = data[0].decode('ascii')
                ret['RA'], ret['DEC'] = _coord_convert(data[1], data[2])
                ret['RA_PREC'] = data[3]
                ret['DEC_PREC'] = data[4]
                ret['COO_ERR_MAJA'] = data[5]
                ret['COO_ERR_MINA'] = data[6]
                ret['COO_ERR_ANGLE'] = data[7]
                ret['COO_QUAL'] = data[8]
                ret['COO_WAVELENGTH'] = data[9]
                ret['COO_BIBCODE'] = data[10]

                return ret
            except Exception as ex:
                self.logger(f'Simbad: {ex}')

        return None

    def run(self):
        for corr_obj in CorrFits.objects.filter(astro_job_id=self.job_number):
            if corr_obj.simbad_data:
                continue
    
            RA = corr_obj.field_ra
            DEC = corr_obj.field_dec

            found_obj = SimbadData.objects.filter(
                RA__range=(RA - self.radius, RA + self.radius),
                DEC__range=(DEC - self.radius, DEC + self.radius),
            )

            if found_obj:
                if len(found_obj) > 1:
                    self.logger(f'Two or more object in SimbadData for RA = {RA} DEC = {DEC} radius {self.radius}')
                else:
                    corr_obj.simbad_data = found_obj[0]
                    corr_obj.save()
            else:
                sim_obj = SimbadData(**self._get_info_from_simbad(RA, DEC))

                if sim_obj:
                    sim_obj.save()

                    corr_obj.simbad_data = sim_obj
                    corr_obj.save()

class AAVSOLoader(ProtoLoader):
    def _get_info_from_aavso(self, obj_name):
        self.rsleep()        

        aavso_format = obj_name.replace(' ', '+').lstrip('V*')

        self.logger(f'Get AAVSO data for {aavso_format}')

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
        aavso_data = aavso_data.get('VSXObject', {})
        self.logger(aavso_data)

        if aavso_data:
            aavso_data['RA2000'] = float(aavso_data['RA2000'])
            aavso_data['Declination2000'] = float(aavso_data['Declination2000'])
            aavso_data['ProperMotionRA'] = float(aavso_data['ProperMotionRA'])
            aavso_data['ProperMotionDec'] = float(aavso_data['ProperMotionDec'])

            if 'Period' in aavso_data:
                aavso_data['Period'] = float(re.sub('[^0-9]','', aavso_data['Period']))

            if 'Epoch' in aavso_data:
                aavso_data['Epoch'] = float(aavso_data['Epoch'])

        return aavso_data

    def run(self):
        for corr_obj in CorrFits.objects.filter(astro_job_id=self.job_number):
            if corr_obj.aavso_data:
                continue

            RA2000 = corr_obj.field_ra
            Declination2000 = corr_obj.field_dec

            found_obj = AAVSOData.objects.filter(
                RA2000__range=(RA2000 - self.radius, RA2000 + self.radius),
                Declination2000__range=(Declination2000 - self.radius, Declination2000 + self.radius),
            )

            if found_obj:
                if len(found_obj) > 1:
                    self.logger(f'Two or more object in AAVSOData for RA2000 = {RA2000} Declination2000 = {Declination2000} radius {self.radius}')
                else:
                    corr_obj.aavso_data = found_obj[0]
                    corr_obj.save()
            else:
                params = self._get_info_from_aavso(corr_obj.simbad_data.MAIN_ID)
                
                if params:
                    aavso_obj = AAVSOData(**params)
                    aavso_obj.save()

                    corr_obj.aavso_data = aavso_obj
                    corr_obj.save()
