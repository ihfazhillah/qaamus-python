import unittest
from bs4 import BeautifulSoup
from ind_ara_parser import BaseParser


class AngkaParser(BaseParser):
    """Handle terjemah angka page."""
    def get_instruction(self):
        """Return the instruction text.

        text is returning 'Terjemah angka adalah menterjemahkan angka
        kedalam bahasa arab, caranya cukup mudah ketik angka
        (tanpa titik dan koma) yang akan di terjemahkan'."""
        text = self.soup.select(".page-header > h1")[0].next_sibling.strip()
        return text.split(",")[1].strip().capitalize()


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

    def test_get_footer(self):
        result = self.angka_parser._get_footer()
        expected = ''
        self.assertEqual(result, expected)

    def test_get_arti_master(self):
        result = self.angka_parser.get_arti_master()
        expected = {"ind": '123',
                    "ara": 'المئة و الثالث و العشرون',
                    "footer": ""}
        self.assertEqual(result, expected)

    def test_get_page_header(self):
        result = self.angka_parser.get_instruction()
        expected = ("Caranya cukup mudah ketik "
                    "angka (tanpa titik dan koma) yang akan di terjemahkan")
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
