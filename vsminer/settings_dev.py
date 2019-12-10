import os

from .settings import BASE_DIR

ALLOWED_HOSTS = ['*']

USE_TZ = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'vsminer',
        'USER': 'vsminer',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

MEDIA_ROOT = os.path.join(BASE_DIR, 'data')
