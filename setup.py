# -*- coding: utf-8 -*-
"""Python packaging."""
from os.path import abspath, dirname, join
from setuptools import setup


def read_relative_file(filename):
    """Returns contents of the given file, which path is supposed relative
    to this module."""
    with open(join(dirname(abspath(__file__)), filename)) as f:
        return f.read()


def packages(project_name):
    """Return list of packages distributed by project based on its name.

    >>> packages('foo')
    ['foo']
    >>> packages('foo.bar')
    ['foo', 'foo.bar']
    >>> packages('foo.bar.baz')
    ['foo', 'foo.bar', 'foo.bar.baz']
    >>> packages('FooBar')
    ['foobar']

    Implements "Use a single name" convention described in :pep:`423`.

    """
    name = str(project_name).lower()
    if '.' in name:  # Using namespace packages.
        parts = name.split('.')
        return ['.'.join(parts[0:i]) for i in range(1, len(parts) + 1)]
    else:  # One root package or module.
        return [name]


def namespace_packages(project_name):
    """Return list of namespace packages distributed in this project, based on
    project name.

    >>> namespace_packages('foo')
    []
    >>> namespace_packages('foo.bar')
    ['foo']
    >>> namespace_packages('foo.bar.baz')
    ['foo', 'foo.bar']
    >>> namespace_packages('Foo.BaR.BAZ') == namespace_packages('foo.bar.baz')
    True

    Implements "Use a single name" convention described in :pep:`423`.

    """
    package_list = packages(project_name)
    package_list.pop()  # Ignore last element.
    # Remaining packages are supposed to be namespace packages.
    return package_list


name = 'django-chunkator'
readme = read_relative_file('README.rst')
requirements = ['six', 'django>=1.11']
entry_points = {}


if __name__ == '__main__':  # ``import setup`` doesn't trigger setup().
    setup(name=name,
          version='1.4.0',
          description="""Chunk large QuerySets into small chunks, and iterate over them without killing your RAM.""",  # noqa
          long_description=readme,
          classifiers=[
              'Environment :: Web Environment',
              'Framework :: Django',
              'Operating System :: OS Independent',
              'Programming Language :: Python',
              'Programming Language :: Python :: 2',
              'Programming Language :: Python :: 2.7',
              'Programming Language :: Python :: 3',
              'Programming Language :: Python :: 3.5',
              'Programming Language :: Python :: 3.6',
              'Programming Language :: Python :: 3.7',
              'Topic :: Internet :: WWW/HTTP',
              'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
              'License :: OSI Approved :: MIT License',
          ],
          keywords='',
          author='PeopleDoc',
          author_email='rd@people-doc.com',
          url='https://github.com/peopledoc/%s' % name,
          license='MIT',
          packages=['chunkator'],
          namespace_packages=namespace_packages(name),
          include_package_data=True,
          zip_safe=False,
          install_requires=requirements,
          entry_points=entry_points,
          )
