import os
import unittest
from bs4 import BeautifulSoup
from parsers import IndAraParser, AngkaParser, PegonParser

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def soupping(file):
    with open(file, 'rb') as f:
        file = f.read()
    return BeautifulSoup(file)


def get_abs_path(path):
    return os.path.join(BASE_DIR, path)


class AraIndParserTest(unittest.TestCase):

    def setUp(self):
        self.soup = soupping(get_abs_path('html/rumah+sakit'))
        self.indaraparser = IndAraParser(self.soup)

    def tearDown(self):
        del self.indaraparser

    def test_get_master_tranlated(self):
        master = self.indaraparser._get_ara()
        self.assertEqual(master, "مستشفى")

    def test_get_master_ind(self):
        master = self.indaraparser._get_query()
        self.assertEqual(master, "rumah sakit")

    def test_get_footer_translation(self):
        master = self.indaraparser._get_footer()
        self.assertEqual(master, "*Diterjemahkan dengan Bing Translator ")

    def test_get_arti_berhub_jumlah(self):
        secondary = self.indaraparser.get_arti_berhub()
        self.assertEqual(len(secondary), 10)

    def test_get_arti_berhub_first(self):
        secondary = self.indaraparser.get_arti_berhub()
        self.assertEqual(secondary[0],
                         {"ind": "rumah sakit gila",
                          "ara": "بَيتُ الـمَجَانِبِينِ، مُسْتَشْفَى الـمَجَانِيْنِ"})

    def test_get_arti_master(self):
        """memberikan kembalian berupa dict, {'ind': indonesia,
        'ara': arabic, 'footer': footer_text}"""
        master = self.indaraparser.get_arti_master()
        self.assertEqual(master, {"ind": "rumah sakit",
                                  "ara": "مستشفى",
                                  "footer": "*Diterjemahkan dengan Bing Translator "})

    def test_get_next_page_url(self):
        url_to = self.indaraparser.get_next_page_url()
        self.assertEqual(url_to, get_abs_path("html/rumah+sakit2"))

    def test_get_next_page_url_with_no_next_in_page(self):
        soup = soupping(get_abs_path("html/rumah+sakit9"))
        no_next = IndAraParser(soup).get_next_page_url()
        self.assertFalse(no_next)

    def test_get_all_kata_berhub(self):
        secondary = self.indaraparser.get_all_arti_berhub(soupping)
        self.assertEqual(len(secondary), 89)


class AngkaParserTestCase(unittest.TestCase):

    def setUp(self):
        self.soup = soupping(get_abs_path("html/angka123"))
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


class PegonTestCase(unittest.TestCase):
    def setUp(self):
        self.soup = soupping(get_abs_path("html/pegon_suratman"))
        self.pegon = PegonParser(self.soup)

    def tearDown(self):
        del self.pegon
        del self.soup

    def test_get_query(self):
        result = self.pegon._get_query()
        expected = "suratman"
        self.assertEqual(result, expected)

    def test_get_ara(self):
        result = self.pegon._get_ara()
        expected = "سوراتمان"
        self.assertEqual(result, expected)

    def test_get_footer(self):
        result = self.pegon._get_footer()
        expected = ""
        self.assertEqual(result, expected)

    def test_get_instruction(self):
        result = self.pegon.get_instruction()
        expected = ("Masukkan nama orang (nama yang bukan dari bahasa arab),"
                    " nama negara, nama kota, nama desa maupun nama lain yang"
                    " ingin di tulis kedalam tulisan arab")
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
