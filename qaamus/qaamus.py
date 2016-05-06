import unittest
import requests
from collections import namedtuple
from bs4 import BeautifulSoup
from parsers import IndAraParser, AngkaParser, PegonParser


IDAR = namedtuple("Idar", ("utama", "berhubungan"))
ANGKA_PEGON = namedtuple("Angka_Pegon", ("hasil"))
INSTRUCTION = namedtuple("Instruction", ("instruksi"))


class pretty_output(object):
    def __init__(self, tuple_obj):
        self.tuple_obj = tuple_obj

    @property
    def header(self):
        return "-= Arti dari {ind_utama} =-".format(
                ind_utama=self.tuple_obj[0][0])

    @property
    def body(self):
        return "{ara_utama}".format(
                ara_utama=self.tuple_obj[0][1])

    @property
    def footer(self):
        footer = self.tuple_obj[0][2]
        return "-= {footer} =-".format(
            footer=footer) if footer is not "" else "_" * len(self.header)

    @property
    def header_berhubungan(self):
        return "-= Arti berhubungan dari {ind_utama} =-".format(
                ind_utama=self.tuple_obj[0][0])

    @property
    def body_berhubungan(self):
        arti = []
        # Note: if the second index is str so that is an instruction

        if hasattr(self.tuple_obj, "berhubungan"):
            for berhubungan in self.tuple_obj.berhubungan:
                a = "{ind} : {ara}".format(ind=berhubungan[0],
                                           ara=berhubungan[1])
                arti.append(a)

        return "\n".join(arti) if arti else arti

    @property
    def instruction(self):
        if hasattr(self.tuple_obj, "instruksi"):
            result = ['-= Instruksi Layanan Terjemah {} =-',
                      self.tuple_obj.instruksi]
            return "\n".join(result)

    def hasil(self):
        hasil = [self.header,
                 self.body,
                 self.footer,
                 "",
                 self.header_berhubungan,
                 self.body_berhubungan]
        return "\n".join(hasil if self.body_berhubungan else hasil[:3])


class PrettyOutputTestCase(unittest.TestCase):
    def setUp(self):
        self.tuple_ = IDAR(("ind_utama", "ara_utama", "footer"),
                           [("ind_pertama", "ara_pertama"),
                            ("ind_kedua", "ara_kedua")])
        self.tuple_angka = ANGKA_PEGON(("1234", "ara_utama", ""),)
        self.tuple_instruction = INSTRUCTION("Ini adalah instruksi")

    def test_pretty_output_header(self):
        po = pretty_output(self.tuple_).header
        expected = "-= Arti dari ind_utama =-"
        self.assertEqual(po, expected)

    def test_pretty_output_arabic(self):
        po = pretty_output(self.tuple_).body
        expected = "ara_utama"
        self.assertEqual(po, expected)

    def test_pretty_output_footer(self):
        po = pretty_output(self.tuple_).footer
        expected = "-= footer =-"
        self.assertEqual(po, expected)

    def test_pretty_output_header_berhubungan(self):
        po = pretty_output(self.tuple_).header_berhubungan
        expected = "-= Arti berhubungan dari ind_utama =-"
        self.assertEqual(po, expected)

    def test_pretty_output_body_berhubungan(self):
        po = pretty_output(self.tuple_).body_berhubungan
        expected = ("ind_pertama : ara_pertama\n"
                    "ind_kedua : ara_kedua")
        self.assertEqual(po, expected)

    def test_pretty_output_hasil(self):
        po = pretty_output(self.tuple_).hasil()
        expected = ("-= Arti dari ind_utama =-\n"
                    "ara_utama\n"
                    "-= footer =-\n"
                    "\n"
                    "-= Arti berhubungan dari ind_utama =-\n"
                    "ind_pertama : ara_pertama\n"
                    "ind_kedua : ara_kedua")
        self.assertEqual(po, expected)

    def test_pretty_output_footer_angka(self):
        po = pretty_output(self.tuple_angka).footer
        expected = "_" * 20
        self.assertEqual(po, expected)

    def test_pretty_output_hasil_angka(self):
        po = pretty_output(self.tuple_angka).hasil()
        expected = ("-= Arti dari 1234 =-\n"
                    "ara_utama\n"
                    "____________________")
        self.assertEqual(po, expected)

    def test_pretty_output_instruction(self):
        po = pretty_output(self.tuple_instruction).instruction.format("Angka")
        expected = ("-= Instruksi Layanan Terjemah Angka =-\n"
                    "Ini adalah instruksi")
        self.assertEqual(po, expected)

    def test_pretty_output_instruction_pegon(self):
        po = pretty_output(self.tuple_instruction).instruction.format("Pegon")
        expected = ("-= Instruksi Layanan Terjemah Pegon =-\n"
                    "Ini adalah instruksi")
        self.assertEqual(po, expected)


class Qaamus:

    def terjemah(self, layanan, query, pretty=False):
        """
        Return terjemahan tergantung dengan **layanan** apa yang dia pilih,
        dan **query** apa yang dia pakai.
        Adapun *layanan* di [Qaamus](qaamus.com) saat ini terdapat 3 layanan:
            * Indonesia Arab
            * Angka
            * Terjemah nama
        Sedangkan *query* adalah query pencarian anda"""
        if layanan == "idar":
            url = self.build_url(query)
            soup = self._make_soup(url)
            parser = IndAraParser(soup)
            result = IDAR(parser.get_arti_master(), parser.get_all_arti_berhub(
                          self._make_soup))
            if not pretty:
                return result
            return pretty_output(result).hasil()

        elif layanan == "angka":
            url = self.build_url(query, layanan)
            soup = self._make_soup(url)
            parser = AngkaParser(soup)
            result = ANGKA_PEGON(parser.get_arti_master())
            if not pretty:
                return result
            return pretty_output(result).hasil()

        elif layanan == "angka_instruction":
            url = self.build_url(query, layanan='angka')
            soup = self._make_soup(url)
            parser = AngkaParser(soup)
            result = INSTRUCTION(parser.get_instruction())
            if not pretty:
                return result
            return pretty_output(result).instruction.format("Angka")

        elif layanan == "pegon":
            url = self.build_url(query, layanan)
            soup = self._make_soup(url)
            parser = PegonParser(soup)
            result = ANGKA_PEGON(parser.get_arti_master())
            if not pretty:
                return result
            return pretty_output(result).hasil()

        elif layanan == "pegon_instruction":
            url = self.build_url(query, layanan='pegon')
            soup = self._make_soup(url)
            parser = PegonParser(soup)
            result = INSTRUCTION(parser.get_instruction())
            if not pretty:
                return result
            return pretty_output(result).instruction.format("Pegon")

    def _make_soup(self, url):
        """Return BeautifulSoup object."""
        resp = requests.get(url)
        return BeautifulSoup(resp.content)

    def build_url(self, query, layanan=None):
        """Return url pencarian sesuai dengan *query* yang dimasukkan.
        layanan ketika None maka akan terjadi pengecekan query,
        kalau query adalah integer atau seperti integer maka berikan kembalian
        ANGKA_URL,
        kalau string maka secara default akan direfrensikan ke INDO_URL.
        Bila tidak None, maka tergantung dengan layanan yang diminta."""

        # syntactic sugar
        is_angka = isinstance(query, int) or query.isdigit()

        ANGKA_URL = "http://qaamus.com/terjemah-angka/{number}/angka".format(
            number=query)
        INDO_URL = "http://qaamus.com/indonesia-arab/{query}/1".format(
            query="+".join(query.split()))
        PEGON_URL = 'http://qaamus.com/terjemah-nama/{pegon}'.format(
            pegon=query)

        layanan_mapping = dict(
            (('angka', ANGKA_URL),
             ('idar', INDO_URL),
             ('pegon', PEGON_URL))
            )

        if not layanan:
            if is_angka:
                url = ANGKA_URL
            elif isinstance(query, str):
                url = INDO_URL
        else:
            if layanan in layanan_mapping:
                url = layanan_mapping[layanan]
            else:
                raise LayananValueError("Layanan tidak ditemukan")

        return url


class LayananValueError(ValueError):
    def __init__(self, message=None):
        super(LayananValueError, self).__init__(message)
        self.message = message


class QaamusTest(unittest.TestCase):

    def test_building_idar_url(self):
        q = Qaamus()
        expected_url = "http://qaamus.com/indonesia-arab/capai/1"
        this_url = q.build_url("capai")
        self.assertEqual(this_url, expected_url)

    def test_building_idar_url_with_multiple_words(self):
        q = Qaamus()
        expected_url = "http://qaamus.com/indonesia-arab/mobil+ambulan+bagus/1"
        this_url = q.build_url("mobil ambulan bagus")
        self.assertEqual(this_url, expected_url)

    def test_building_angka_url(self):
        q = Qaamus()
        expected_url = "http://qaamus.com/terjemah-angka/123/angka"
        this_url = q.build_url("123")
        self.assertEqual(this_url, expected_url)

    def test_building_pegon_url(self):
        q = Qaamus()
        expected_url = "http://qaamus.com/terjemah-nama/suratman"
        this_url = q.build_url("suratman", "pegon")
        self.assertEqual(this_url, expected_url)

    def test_building_angka_url_with_layanan(self):
        q = Qaamus()
        expected_url = "http://qaamus.com/terjemah-angka/123/angka"
        this_url = q.build_url("123", 'angka')
        self.assertEqual(this_url, expected_url)

    def test_building_idar_url_with_multiple_words_with_layanan(self):
        q = Qaamus()
        expected_url = "http://qaamus.com/indonesia-arab/mobil+ambulan+bagus/1"
        this_url = q.build_url("mobil ambulan bagus", 'idar')
        self.assertEqual(this_url, expected_url)

    def test_building_idar_url_with_layanan(self):
        q = Qaamus()
        expected_url = "http://qaamus.com/indonesia-arab/capai/1"
        this_url = q.build_url("capai", 'idar')
        self.assertEqual(this_url, expected_url)

    def test_building_url_with_wrong_layanan(self):
        q = Qaamus()
        try:
            q.build_url("capai", "lainnya")
        except LayananValueError as L:
            self.assertEqual(L.message, "Layanan tidak ditemukan")


if __name__ == "__main__":
    unittest.main()
