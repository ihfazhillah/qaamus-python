# -*- coding: utf-8 -*-
import unittest
from qaamus.parsers import (IndAraParser,
                            AngkaParser,
                            PegonParser,
                            TemplateParser)
from qaamus.out import Result
from qaamus.utils import soupping, get_abs_path


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
        self.assertEqual(len(secondary.berhubungan), 10)

    def test_get_next_page_url(self):
        url_to = self.indaraparser.get_next_page_url()
        self.assertEqual(url_to, get_abs_path("html/rumah+sakit2"))

    def test_get_next_page_url_with_no_next_in_page(self):
        soup = soupping(get_abs_path("html/rumah+sakit9"))
        no_next = IndAraParser(soup).get_next_page_url()
        self.assertFalse(no_next)

    def test_get_all_kata_berhub(self):
        secondary = self.indaraparser.get_all_arti_berhub(soupping)
        self.assertEqual(len(secondary.berhubungan), 89)

    def test_get_hasil_return_Result_instance(self):
        hasil = self.indaraparser.get_arti_master()
        self.assertTrue(isinstance(hasil, Result))
        self.assertEqual(hasil.utama, (
                                  "rumah sakit",
                                  "مستشفى",
                                  "*Diterjemahkan dengan Bing Translator "))

    def test_get_arti_berhub_first_Result_instance(self):
        secondary = self.indaraparser.get_arti_berhub()
        self.assertTrue(isinstance(secondary, Result))
        self.assertEqual(secondary.berhubungan[0],
                         ("rumah sakit gila",
                          "بَيتُ الـمَجَانِبِينِ، مُسْتَشْفَى الـمَجَانِيْنِ"))

    def test_get_all_kata_berhub_Result_instance(self):
        secondary = self.indaraparser.get_all_arti_berhub(soupping)
        self.assertEqual(len(secondary.berhubungan), 89)

    def test_get_idar(self):
        hasil = self.indaraparser.get_idar(soupping)
        self.assertTrue(hasil.berhubungan)
        self.assertTrue(hasil.utama)


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

    def test_get_instruction_Result_instance(self):
        result = self.angka_parser.get_instruction()
        expected = ("Caranya cukup mudah ketik "
                    "angka (tanpa titik dan koma) yang akan di terjemahkan")
        self.assertTrue(isinstance(result, Result))
        self.assertEqual(result.instruksi, expected)


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

    def test_get_instruction_Result_instance(self):
        result = self.pegon.get_instruction()
        expected = ("Masukkan nama orang (nama yang bukan dari bahasa arab),"
                    " nama negara, nama kota, nama desa maupun nama lain yang"
                    " ingin di tulis kedalam tulisan arab")
        self.assertTrue(isinstance(result, Result))
        self.assertEqual(result.instruksi, expected)


class TemplateParserTestCase(unittest.TestCase):
    sample_text = """####first####
this first
this first val
this first val val
####second####
this second val
this second val
this seeeeeecond val"""

    def splitting_text(self):
        return self.sample_text.split("\n")

    def test_get_keys_and_pos(self):
        parser = TemplateParser(self.splitting_text())
        self.assertEqual(parser.keys(), [('first', 0), ('second', 4)])

    def test_get_first_val(self):
        parser = TemplateParser(self.splitting_text())
        expected = "this first\nthis first val\nthis first val val"
        self.assertEqual(parser.result().first, expected)


if __name__ == "__main__":
    unittest.main()
