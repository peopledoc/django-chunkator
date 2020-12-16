================
django-chunkator
================


Chunk large QuerySets into small chunks, and iterate over them without killing
your RAM.

.. image:: https://travis-ci.org/peopledoc/django-chunkator.svg

Tested with all the combinations of:

* Python: 3.6, 3.7, 3.8
* Django: 2, 2.1, 2.2, 3.0, master

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


FAQ
===

- How is django-chunkator different from Django's `iterator <https://docs.djangoproject.com/en/2.2/ref/models/querysets/#django.db.models.query.QuerySet.iterator>`_?

If you have server-side cursors (using Postgres or Oracle & not setting `DISABLE_SERVER_SIDE_CURSORS`), then the main difference is that the cursor is in the hands of the application instead of the server. It really depends on your constraints, but sometimes server side cursors can put too much strains on your DB.

If you don't have server-side cursors, then chunkator will allow you to iterate over your queryset by batch, without relying on LIMIT/OFFSET. The problem with LIMIT/OFFSET is that computing a large offset (when you're at the end of your queryset) requires the DB to go through all the previous entries. With large tables this can be a huge issue.

- Will django-chunkator preserve the ordering on my querysets?

No, it orders the queryset by pk. However you could do the same thing than chunkator with another field, given that it's unique and not nullable, see `here <https://github.com/peopledoc/django-chunkator/blob/master/chunkator/__init__.py#L27-L33>`_ for more details.


License
=======

MIT License.
