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


def chunkator(source_qs, chunk_size, query_log=None):
    """
    Yield over a queryset by chunks.

    This method does not involve counting elements or measuring the iterable
    length. We're saving at least a ``count()`` query on QuerySets, or a
    CPU-and-RAM-consuming ``len(queryset)`` query.
    """
    pk = None
    if isinstance(source_qs, ValuesQuerySet):
        if "pk" not in source_qs._fields:
            raise MissingPkFieldException("The values() call must include the `pk` field")  # noqa

    source_qs = source_qs.order_by('pk')
    queryset = source_qs
    while True:
        if pk:
            queryset = source_qs.filter(pk__gt=pk)
        page = queryset[:chunk_size]
        if query_log is not None:
            query_log.write(unicode(page.query) + "\n")
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
