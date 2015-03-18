from django.test import TestCase
from chunkator import chunkator
from demo_chunkator.models import Book


class ChunkatorTestCase(TestCase):

    def setUp(self):
        super(ChunkatorTestCase, self).setUp()
        for nb in range(20):
            Book.objects.create(
                title="Title #{}".format(nb),
                author="Author #{}".format(nb)
            )

    def test_chunks_queryset(self):
        # small step
        chunks = chunkator(Book.objects.all(), 1)
        result = []
        for item in chunks:
            self.assertTrue(isinstance(item, Book))
            result.append(item.pk)
        self.assertEquals(len(result), 20)
        self.assertEquals(len(result), len(set(result)))  # no duplicates

        result = []
        # larger chunks
        chunks = chunkator(Book.objects.all(), 10)
        for item in chunks:
            self.assertTrue(isinstance(item, Book))
            result.append(item.pk)
        self.assertEquals(len(result), 20)
        self.assertEquals(len(result), len(set(result)))  # no duplicates

        result = []
        # larger than QS chunks
        chunks = chunkator(Book.objects.all(), 50)
        for item in chunks:
            self.assertTrue(isinstance(item, Book), "{}".format(item))
            result.append(item.pk)
        self.assertEquals(len(result), 20)
        self.assertEquals(len(result), len(set(result)))  # no duplicates

    def test_chunks_numqueries(self):
        # Make sure we only run 2 queries
        # One for each slice
        with self.assertNumQueries(2):
            chunks = chunkator(Book.objects.all(), 12)
            for item in chunks:
                self.assertTrue(isinstance(item, Book))

        # Make sure we only run 3 queries
        # One for each slice, plus the "empty" one
        with self.assertNumQueries(3):
            chunks = chunkator(Book.objects.all(), 10)
            for item in chunks:
                self.assertTrue(isinstance(item, Book))
