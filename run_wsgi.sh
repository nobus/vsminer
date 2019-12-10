#!/bin/bash

$HOME/.virtualenvs/vsminer/bin/uwsgi --socket wsgi.sock --module vsminer.wsgi --chmod-socket=666
