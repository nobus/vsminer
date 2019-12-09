# -*- coding: utf-8 -*-

import os
import sys
import json
import requests

import shutil

import numpy as np
import msgpack
import msgpack_numpy as m
m.patch()

import matplotlib
import matplotlib.pyplot as plt

from astropy.io import fits
from astropy.utils.data import download_file

from django.core.management.base import BaseCommand
from django.conf import settings

from vs_app.models import AstroMetryJob, CorrFits


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--job-number', dest='job_number', type=int, help='job number')
        parser.add_argument('--status-url', dest='status_url', type=str, help='status url')

        parser.add_argument('--job-info', dest='job_info', help='get job info', action='store_true')
        parser.add_argument('--new-image', dest='new_image', help='get new_image.fits', action='store_true')
        parser.add_argument('--corr-image', dest='corr', help='get corr.fits', action='store_true')
        parser.add_argument('--all', dest='all', help='get all', action='store_true')


    def get_job_info(self):
        """
        http://astrometry.net/doc/net/api.html#getting-job-results
        """

        print(f'Get job info for job={self.job_number}')
        resp = requests.get(f'http://nova.astrometry.net/api/jobs/{self.job_number}/info/')

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

    def _minmax_calc(self, image_data):
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

    def get_new_image(self):
        fits_fpath = self._download_file('new_fits')
        hdu_list = fits.open(fits_fpath)

        if hdu_list:
            image_data = hdu_list[0].data
            vmin, vmax = self._minmax_calc(image_data)

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
            print('No image data', file=sys.stderr)

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

    def handle(self, *args, **options):
        self.job_number = options['job_number']
        self.status_url = options['status_url']

        self.astrometry_url = 'http://nova.astrometry.net'
        self.job_dir = os.path.join(settings.MEDIA_ROOT, str(self.job_number))

        if not os.path.exists(self.job_dir):
            os.mkdir(self.job_dir)

        if options['all']:
            self.get_all()
        else:
            if options['job_info']:
                self.get_job_info()

            if options['new_image']:
                self.get_new_image()

            if options['corr']:
                self.get_corr()
