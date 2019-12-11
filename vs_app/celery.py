# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from django.conf import settings
from celery import Celery

# https://docs.celeryproject.org/en/latest/getting-started/brokers/redis.html#broker-redis
app = Celery('vs_app',
             broker='amqp://guest@localhost//',
             backend='redis://localhost',
             include=['vs_app.tasks'])

app.conf.broker_transport_options = {'visibility_timeout': 43200}

#app.conf.broker_url = 'redis://localhost:6379/0'
#app.conf.result_backend = 'redis://localhost:6379/0'

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

app.conf.task_serializer = 'json'
app.conf.result_serializer = 'json'


if __name__ == '__main__':
    app.start()
