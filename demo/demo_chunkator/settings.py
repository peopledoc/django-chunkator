# -*- coding: utf-8 -*-

INSTALLED_APPS = [
    'demo_chunkator',
]

# Databases.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'demo_chunkator.db',
    }
}

# URL configuration.
ROOT_URLCONF = 'demo_chunkator.urls'

# Fake secret key.
SECRET_KEY = 'Fake secret.'

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
)
