# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import time

from .celery import app


@app.task
def sleep(n):
    # test task

    for i in range(n):
        print(i)
        time.sleep(1)

    return {'n': n}
