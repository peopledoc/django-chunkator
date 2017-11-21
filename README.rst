================
django-chunkator
================


Chunk large QuerySets into small chunks, and iterate over them without killing
your RAM.

.. image:: https://travis-ci.org/peopledoc/django-chunkator.svg

Tested with all the combinations of:

* Python: 2.7, 3.4, 3.5.
* Django: 1.8 (LTS), 1.9, 1.10, 1.11.

Also, tested the following:

* Python 3.6 + Django 1.11
* Python 3.4, 3.5, 3.6 + Django "master".

Usage
=====

.. code:: python

    from chunkator import chunkator
    for item in chunkator(LargeModel.objects.all(), 200):
        do_something(item)

This tool is intended to work on Django querysets.

Your model **must** define a ``pk`` field (this is done by default, but
sometimes it can be overridden) and this pk has to be unique. ``django-
chunkator`` has been tested with PostgreSQL and SQLite, using regular PKs and
UUIDs as primary keys.

You can also use ``values()``:

.. code:: python

    from chunkator import chunkator
    for item in chunkator(LargeModel.objects.values('pk', 'name'), 200):
        do_something(item)

.. important::

    If you're using ``values()`` you **have** to add at least your "pk" field
    to the values, otherwise, the chunkator will throw a
    ``MissingPkFieldException``.

.. warning::

    This will not **accelerate** your process. Instead of having one BIG query,
    you'll have several small queries. This will save your RAM instead, because
    you'll not load a huge queryset result before looping on it.

If you want to manipulate the pages directly, you can use `chunkator_page`:

.. code:: python

    from chunkator import chunkator_page
    queryset = LargeModel.objects.all().values('pk')
    for page in chunkator_page(queryset, 200):
        launch_some_task([item['pk'] for item in page])

License
=======

MIT License.
