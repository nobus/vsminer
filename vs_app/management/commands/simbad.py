# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from vs_app.downloaders import SimbadLoader

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--job-number', dest='job_number', type=int, help='job number')

    def handle(self, *args, **options):
        simbad_loader = SimbadLoader(options['job_number'])
        simbad_loader.run()
