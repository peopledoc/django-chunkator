from django.test import TestCase
from chunkator import chunkator
from demo_chunkator.models import Book, User


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


class ChunkatorOrderTestCase(TestCase):
    def setUp(self):
        super(ChunkatorOrderTestCase, self).setUp()
        Book.objects.create(
            title="Guards! Guards!",
            author="Pratchett, Terry"
        )
        Book.objects.create(
            title="The Player of Games",
            author="Banks, Iain"
        )

    def test_order_by_default(self):
        items = list(chunkator(Book.objects.all(), 10))
        self.assertEquals(items[0].pk, 1)
        self.assertEquals(items[1].pk, 2)


class ChunkatorUUIDTestCase(TestCase):

    def setUp(self):
        super(ChunkatorUUIDTestCase, self).setUp()
        User.objects.create(name='Terry Pratchett')
        User.objects.create(name='Iain Banks')

    def test_chunk_uuid(self):
        result = []
        chunks = chunkator(User.objects.all(), 10)
        for item in chunks:
            self.assertTrue(isinstance(item, User))
            result.append(item.pk)
        self.assertEquals(len(result), 2)
        self.assertEquals(len(result), len(set(result)))  # no duplicates


class ChunkatorValuesTestCase(TestCase):

    def setUp(self):
        super(ChunkatorValuesTestCase, self).setUp()
        User.objects.create(name='Wonder Woman')
        User.objects.create(name='Wolverine')

    def test_chunk_uuid(self):
        result = []
        chunks = chunkator(User.objects.all().values("pk", "name"), 10)
        for item in chunks:
            self.assertTrue(isinstance(item, dict))
            result.append(item['pk'])
        self.assertEquals(len(result), 2)
        self.assertEquals(len(result), len(set(result)))  # no duplicates
