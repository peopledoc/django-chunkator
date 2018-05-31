# -*- coding: utf-8 -*-
from os.path import abspath, dirname, join
_current_dir = dirname(abspath(__file__))

INSTALLED_APPS = [
    'demo_chunkator',
]

# Databases.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(_current_dir, 'demo_chunkator.db'),
    }
}

# URL configuration.
ROOT_URLCONF = 'demo_chunkator.urls'

# Fake secret key.
SECRET_KEY = 'Fake secret.'

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

MIDDLEWARE = (
    'django.middleware.common.CommonMiddleware',
)
