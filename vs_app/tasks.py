# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import time

from .celery import app
from celery.utils.log import get_task_logger

from vs_app.downloaders import AstrometryLoader, SimbadLoader, AAVSOLoader


task_logger = get_task_logger(__name__)

def logger(mess):
    task_logger.info(mess)

@app.task
def sleep(n):
    # test task

    for i in range(n):
        logger(f'Current iteration: {i}')
        time.sleep(1)

    return {'n': n}

@app.task
def download_astrometry_data(job_number, status_url):
    astro_loader = AstrometryLoader(logger, job_number, status_url)
    simbad_loader = SimbadLoader(logger, job_number)
    aavso_loader = AAVSOLoader(logger, job_number)

    astro_loader.run()
    simbad_loader.run()
    aavso_loader.run()

    return {'status': 'success'}
