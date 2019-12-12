#!/bin/bash

export DJANGO_SETTINGS_MODULE=vsminer.settings

celery flower -A vs_app --address=127.0.0.1 --port=5555
