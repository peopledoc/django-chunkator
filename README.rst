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

Warnings:

* This toolkit will only work if your models use "pk" as their primary key
  **and** that this primary key is an integer (no UUID, or such),
* This will not **accelerate** your process. Instead of having one BIG query,
  you'll have several small queries. This will save your RAM instead, because
  you'll not load a huge queryset result before looping on it.
