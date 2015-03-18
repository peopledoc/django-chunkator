# -*- coding: utf-8 -*-
"""Python packaging."""
import os
from setuptools import setup


here = os.path.abspath(os.path.dirname(__file__))

NAME = u'demo_chunkator'
DESCRIPTION = u'Demo for django-chunkator.'
PACKAGES = ['demo_chunkator']
REQUIREMENTS = [
    'django',
    'django-chunkator',
]
AUTHOR = u'Novapost'
EMAIL = u'rd@novapost.fr'
CLASSIFIERS = []
KEYWORDS = []
ENTRY_POINTS = {
    'console_scripts': ['rundemo = demo_chunkator.manage:main'],
}

if __name__ == '__main__':  # Don't run setup() when we import this module.
    setup(name=NAME,
          version='0.0.1',
          description=DESCRIPTION,
          classifiers=CLASSIFIERS,
          keywords=' '.join(KEYWORDS),
          author=AUTHOR,
          author_email=EMAIL,
          packages=PACKAGES,
          include_package_data=True,
          zip_safe=False,
          install_requires=REQUIREMENTS,
          entry_points=ENTRY_POINTS)
