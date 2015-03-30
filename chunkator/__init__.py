"""
Toolbox for chunking / slicing querysets
"""
from django.db.models.query import ValuesQuerySet


class MissingPkFieldException(Exception):
    """
    Exception raised when the "pk" field is missing in the query.

    (when using ``values()``).
    """
    pass


def chunkator(queryset, chunk_size):
    """
    Yield over a queryset by chunks.

    This method does not involve counting elements or measuring the iterable
    length. We're saving at least a ``count()`` query on QuerySets, or a
    CPU-and-RAM-consuming ``len(queryset)`` query.
    """
    pk = None
    if isinstance(queryset, ValuesQuerySet):
        if "pk" not in queryset._fields:
            raise MissingPkFieldException("The values() call must include the `pk` field")  # noqa

    while True:
        queryset = queryset.order_by('pk')
        if pk:
            queryset = queryset.filter(pk__gt=pk)
        page = queryset[:chunk_size]
        nb_items = 0
        for item in page:
            if isinstance(queryset, ValuesQuerySet):
                pk = item["pk"]
            else:
                pk = item.pk
            nb_items += 1
            yield item
        if nb_items < chunk_size:
            raise StopIteration
