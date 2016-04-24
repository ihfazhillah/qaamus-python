import os
import unittest
from bs4 import BeautifulSoup
from ind_ara_parser import IndAraParser

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class AraIndParserTest(unittest.TestCase):
    def get_abs_path(self, path):
        return os.path.join(BASE_DIR, path)

    def soupping(self, file):
        with open(file, 'rb') as f:
            file = f.read()
        return BeautifulSoup(file)

    def setUp(self):
        self.soup = self.soupping(self.get_abs_path('html/rumah+sakit.html'))
        self.indaraparser = IndAraParser(self.soup)

    def test_get_master_tranlated(self):
        master = self.indaraparser.get_ara_master()
        self.assertEqual(master, "مستشفى")

    def test_get_master_ind(self):
        master = self.indaraparser.get_ind_master()
        self.assertEqual(master, "rumah sakit")

    def test_get_footer_translation(self):
        master = self.indaraparser.get_footer_master()
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
        self.assertEqual(url_to, self.get_abs_path("html/rumah+sakit2.html"))

    def test_get_next_page_url_with_no_next_in_page(self):
        soup = self.soupping(self.get_abs_path("html/rumah+sakit9.html"))
        no_next = IndAraParser(soup).get_next_page_url()
        self.assertFalse(no_next)

    def test_get_all_kata_berhub(self):
        secondary = self.indaraparser.get_all_arti_berhub(self.soupping)
        self.assertEqual(len(secondary), 89)


if __name__ == "__main__":
    unittest.main()
