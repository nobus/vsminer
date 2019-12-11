#!/bin/bash

celery flower -A vs_app --address=127.0.0.1 --port=5555
