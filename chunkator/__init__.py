"""
Toolbox for chunking / slicing querysets
"""
import warnings

from distutils.version import StrictVersion
import django

if StrictVersion(django.get_version()) < StrictVersion('1.8.0'):
    with warnings.catch_warnings():
        # This will force the warning to be triggered.
        warnings.simplefilter("always")
        warnings.warn(
            "Django 1.7 and lower versions will soon be deprecated. Please upgrade.",  # noqa
            PendingDeprecationWarning
        )


class MissingPkFieldException(Exception):
    """
    Exception raised when the "pk" field is missing in the query.

    (when using ``values()``).
    """
    pass


def chunkator(source_qs, chunk_size, query_log=None):
    """
    Yield over a queryset by chunks.

    This method does not involve counting elements or measuring the iterable
    length. We're saving at least a ``count()`` query on QuerySets, or a
    CPU-and-RAM-consuming ``len(queryset)`` query.
    """
    pk = None
    # In django 1.9, _fields is always present and `None` if 'values()' is used
    # In Django 1.8 and below, _fields will only be present if using `values()`
    has_fields = hasattr(source_qs, '_fields') and source_qs._fields
    if has_fields:
        if "pk" not in source_qs._fields:
            raise MissingPkFieldException("The values() call must include the `pk` field")  # noqa

    source_qs = source_qs.order_by('pk')
    queryset = source_qs
    while True:
        if pk:
            queryset = source_qs.filter(pk__gt=pk)
        page = queryset[:chunk_size]
        if query_log is not None:
            query_log.write('{page.query}\n'.format(page=page))
        nb_items = 0
        for item in page:
            # source_qs._fields exists *and* is not none when using "values()"
            if has_fields:
                pk = item["pk"]
            else:
                pk = item.pk
            nb_items += 1
            yield item
        if nb_items < chunk_size:
            raise StopIteration
