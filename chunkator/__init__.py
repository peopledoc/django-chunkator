"""
Toolbox for chunking / slicing querysets
"""


def chunkator(queryset, chunk_size):
    """
    Yield over a queryset by chunks.

    This method does not involve counting elements or measuring the iterable
    length. We're saving at least a ``count()`` query on QuerySets, or a
    CPU-and-RAM-consuming ``len(queryset)`` query.
    """
    pk = 0
    while True:
        page = queryset.filter(pk__gt=pk).order_by('pk')[:chunk_size]
        nb_items = 0
        for item in page:
            pk = item.pk
            nb_items += 1
            yield item
        if nb_items < chunk_size:
            raise StopIteration
