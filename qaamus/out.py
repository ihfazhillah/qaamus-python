import unittest


class Result(object):
    def __init__(self, query=None, ara=None, footer=None):
        self.query = query
        self.ara = ara
        self.footer = footer


class ResultTestCase(unittest.TestCase):

    def test_result_with_none_input(self):
        result = Result()
        self.assertEqual(result.query, None)
        self.assertEqual(result.ara, None)
        self.assertEqual(result.footer, None)

    def test_result_with_result_input(self):
        """query, ara, footer object."""
        result = Result("ind_utama", "ara_utama", "footer")
        self.assertEqual(result.query, "ind_utama")
        self.assertEqual(result.ara, "ara_utama")
        self.assertEqual(result.footer, "footer")
