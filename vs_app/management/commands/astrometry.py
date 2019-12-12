# -*- coding: utf-8 -*-

import sys
from django.core.management.base import BaseCommand

from vs_app.downloaders import AstrometryLoader

from . import logger

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--job-number', dest='job_number', type=int, help='job number')
        parser.add_argument('--status-url', dest='status_url', type=str, help='status url')

        parser.add_argument('--job-info', dest='job_info', help='get job info', action='store_true')
        parser.add_argument('--new-image', dest='new_image', help='get new_image.fits', action='store_true')
        parser.add_argument('--corr-image', dest='corr_image', help='get corr.fits', action='store_true')
        parser.add_argument('--all', dest='all', help='get all', action='store_true')

    def handle(self, *args, **options):
        astrometry_loader = AstrometryLoader(
            logger,
            options['job_number'],
            options['status_url'],
            job_info=options['job_info'],
            new_image=options['new_image'],
            corr_image=options['corr_image'],
            all_data=options['all']
        )

        astrometry_loader.run()
