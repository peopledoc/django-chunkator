django-chunkator
================


Chunk large querysetsinto small chunks, and iterate over them without killing
your RAM.

.. image:: https://travis-ci.org/novafloss/django-chunkator.svg

Usage::

    from chunkator import chunkator
    for item in chunkator(LargeModel.objects.all(), 200):
        do_something(item)

This tool is intended to work on Django querysets.
Your model **must** define a pk field (this is done by default, but sometimes
it can be overridden) and this pk has to be unique. ``django-chunkator`` has
been tested with Postgresql and SQLite, using regular PKs and UUIDs as primary
keys.

You can also use ``values()``::

    from chunkator import chunkator
    for item in chunkator(LargeModel.objects.values('pk', 'name'), 200):
        do_something(item)

.. important::

    If you're using ``values`` you **have** to add at least your "pk" field to
    the values, otherwise, the chunkator will throw a `MissingPkFieldException`.

----

.. warning::

    This will not **accelerate** your process. Instead of having one BIG query,
    you'll have several small queries. This will save your RAM instead, because
    you'll not load a huge queryset result before looping on it.
