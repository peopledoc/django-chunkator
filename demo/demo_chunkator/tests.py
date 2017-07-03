import six

from django.test import TestCase

from chunkator import MissingPkFieldException
from chunkator import chunkator
from chunkator import chunkator_page
from demo_chunkator.models import Book
from demo_chunkator.models import Cover
from demo_chunkator.models import Profile
from demo_chunkator.models import User


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
        self.assertEqual(len(result), 20)
        self.assertEqual(len(result), len(set(result)))  # no duplicates

        result = []
        # larger chunks
        chunks = chunkator(Book.objects.all(), 10)
        for item in chunks:
            self.assertTrue(isinstance(item, Book))
            result.append(item.pk)
        self.assertEqual(len(result), 20)
        self.assertEqual(len(result), len(set(result)))  # no duplicates

        result = []
        # larger than QS chunks
        chunks = chunkator(Book.objects.all(), 50)
        for item in chunks:
            self.assertTrue(isinstance(item, Book), "{}".format(item))
            result.append(item.pk)
        self.assertEqual(len(result), 20)
        self.assertEqual(len(result), len(set(result)))  # no duplicates

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

        # If the chunk size is bigger than the number of items, only one query.
        with self.assertNumQueries(1):
            chunks = chunkator(Book.objects.all(), 1000)
            for item in chunks:
                self.assertTrue(isinstance(item, Book))


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
        self.assertEqual(len(result), 2)
        self.assertEqual(len(result), len(set(result)))  # no duplicates


class ChunkatorOrderTestCase(TestCase):
    def setUp(self):
        super(ChunkatorOrderTestCase, self).setUp()
        book = Book.objects.create(
            title="The Player of Games",
            author="Banks, Iain"
        )
        Cover.objects.create(book=book, code='player')
        book = Book.objects.create(
            title="Guards! Guards!",
            author="Pratchett, Terry"
        )
        Cover.objects.create(book=book, code='guards')

        user = User.objects.create(name='Wonder Woman')
        Profile.objects.create(user=user, avatar='wonderful')
        user = User.objects.create(name='Wolverine')
        Profile.objects.create(user=user, avatar='wolfy')

    def test_order_by_default(self):
        items = list(chunkator(Book.objects.all(), 10))
        self.assertEqual(items[0].pk, 1)
        self.assertEqual(items[1].pk, 2)

        uuids = sorted(User.objects.values_list('pk', flat=True))
        items = list(chunkator(User.objects.all(), 10))
        self.assertEqual(items[0].pk, uuids[0])
        self.assertEqual(items[1].pk, uuids[1])

    def test_order_by_with_onetoone_pk(self):
        items = list(chunkator(Cover.objects.all(), 10))
        self.assertEqual(items[0].pk, 1)
        self.assertEqual(items[1].pk, 2)

        items = list(chunkator(Cover.objects.all(), 10))
        self.assertEqual(items[0].pk, 1)
        self.assertEqual(items[1].pk, 2)


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
        self.assertEqual(len(result), 2)
        self.assertEqual(len(result), len(set(result)))  # no duplicates

    def test_chunk_missing_pk(self):
        with self.assertRaises(MissingPkFieldException):
            result = chunkator(User.objects.all().values("name"), 10)
            six.next(result)


class ChunkatorWhereTest(TestCase):
    def setUp(self):
        super(ChunkatorWhereTest, self).setUp()
        User.objects.create(name='Wonder Woman')
        User.objects.create(name='Wolverine')
        User.objects.create(name='ChuckNorris')

    def test_query_log(self):
        query_log_output = six.StringIO()
        qs = User.objects.all()
        # We loop here only to dig into the generator and force execution
        for item in chunkator(qs, 1, query_log=query_log_output):
            _ = item  # noqa
        contents = query_log_output.getvalue()
        query_log_output.close()
        queries = contents.split('\n')
        self.assertEqual(len(queries), 5, queries)
        queries = queries[:4]  # the last one is empty string
        for query in queries:
            # Should be 0 for the first query
            # Should occur once for other queries
            self.assertTrue(query.count('."uuid" >') <= 1, query)


class ChunkatorPageTest(TestCase):
    def setUp(self):
        super(ChunkatorPageTest, self).setUp()
        for nb in range(3):
            Book.objects.create(
                title="Title #{}".format(nb),
                author="Author #{}".format(nb)
            )

    def test_chunkator_page(self):
        qs = Book.objects.all().values('pk')
        pages = list(chunkator_page(qs, 2))
        self.assertEqual(pages, [[{'pk': 1}, {'pk': 2}], [{'pk': 3}]])
