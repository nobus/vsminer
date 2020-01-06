#!/bin/bash

# IRIS 5.59, Canon EOS 1300D, Jupiter 37A, ISO=400, exp=30''

# 3850026   'http://nova.astrometry.net/user_images/3302553#annotated'
# 3850029   'http://nova.astrometry.net/user_images/3302556#annotated'
# 3850033   'http://nova.astrometry.net/user_images/3302560#annotated'

JOB_NUMBER=3850033
STATUS_URL='http://nova.astrometry.net/user_images/3302560#annotated'

python manage.py astrometry --job-number $JOB_NUMBER --status-url $STATUS_URL --all
python manage.py simbad --job-number $JOB_NUMBER
python manage.py aavso --job-number $JOB_NUMBER
