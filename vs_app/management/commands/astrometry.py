# -*- coding: utf-8 -*-

import sys
import json
import requests

import shutil

import msgpack
import msgpack_numpy as m
m.patch()

import matplotlib
import matplotlib.pyplot as plt

from astropy.io import fits
from astropy.utils.data import download_file

from django.core.management.base import BaseCommand

from vs_app.models import AstroMetryJob


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--job-number', dest='job_number', type=int, help='job number')
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

            if not created:
                obj.center_ra = calibration['ra']
                obj.center_dec = calibration['dec']

            obj.save()
        else:
            raise BaseException(f'Job {self.job_id} has wrong status: {job_stat}')

    def get_new_image(self):
        pass

    def get_corr(self):
        pass

    def get_all(self):
        self.get_job_info()
        self.get_new_image()
        self.get_corr()

    def handle(self, *args, **options):
        self.job_number = options['job_number']

        if options['all']:
            self.get_all()
        else:
            if options['job_info']:
                self.get_job_info()

            if options['new_image']:
                self.get_new_image()

            if options['corr']:
                self.get_corr()
