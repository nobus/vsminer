# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from vs_app.downloaders import AAVSOLoader

from . import logger

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--job-number', dest='job_number', type=int, help='job number')

    def handle(self, *args, **options):
        aavso_loader = AAVSOLoader(logger, options['job_number'])
        aavso_loader.run()
