#!/bin/bash

# RAWTRAN 0.3.8, Munipack 0.5.10, IRIS 5.59, Canon EOS 1300D, Jupiter 37A, ISO=400, exp=30''

JOB_NUMBER=$1
STATUS_URL=$2

python manage.py astrometry --job-number $JOB_NUMBER --status-url $STATUS_URL --all
python manage.py simbad --job-number $JOB_NUMBER
python manage.py aavso --job-number $JOB_NUMBER
