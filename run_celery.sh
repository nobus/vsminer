#!/bin/bash

: '
 workon vsminer
 python manage.py shell
 from vs_app import tasks
 result = tasks.sleep.delay(120)
'

celery -A vs_app worker --loglevel=debug
