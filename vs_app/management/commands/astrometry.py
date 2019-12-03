# -*- coding: utf-8 -*-

import sys
import json
import requests

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--job-id', dest='job_id', type=int, help='job id')
        parser.add_argument('--job-info', dest='job_info', help='get job info', action='store_true')
        parser.add_argument('--new-image', dest='new_image', help='get new_image.fits', action='store_true')
        parser.add_argument('--corr-image', dest='corr', help='get corr.fits', action='store_true')
        parser.add_argument('--all', dest='all', help='get all', action='store_true')

    def get_job_info(self):
        """
        http://astrometry.net/doc/net/api.html#getting-job-results
        """

        print(f'Get job info for job={self.job_id}')
        resp = requests.get(f'http://nova.astrometry.net/api/jobs/{self.job_id}/info/')

        job_info = json.loads(resp.text)
        job_stat = job_info.get('status', '')

        if job_stat == 'success':
            print(job_info)
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
        self.job_id = options['job_id']

        if options['all']:
            self.get_all()
        else:
            if options['job_info']:
                self.get_job_info()

            if options['new_image']:
                self.get_new_image()

            if options['corr']:
                self.get_corr()
