import unittest
from bs4 import BeautifulSoup
from ind_ara_parser import BaseParser


class AngkaParser(BaseParser):
    pass


class AngkaParserTestCase(unittest.TestCase):
    with open("../html/angka123", "rb") as f:
        f = f.read()
    soup = BeautifulSoup(f)

    def setUp(self):
        self.angka_parser = AngkaParser(self.soup)

    def test_get_angka(self):
        result = self.angka_parser._get_query()
        expected = '123'
        self.assertEqual(result, expected)

    def test_get_ara(self):
        result = self.angka_parser._get_ara()
        expected = 'المئة و الثالث و العشرون'
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
