import unittest
import requests
from bs4 import BeautifulSoup
from parsers import IndAraParser, AngkaParser


class pretty_output(object):
    def __init__(self, dict_obj):
        self.dict_obj = dict_obj

    @property
    def header(self):
        return "-= Arti dari {ind_utama} =-".format(
                ind_utama=self.dict_obj.get("utama").get("ind"))

    @property
    def body(self):
        return "{ara_utama}".format(
                ara_utama=self.dict_obj.get("utama").get("ara"))

    @property
    def footer(self):
        footer = self.dict_obj.get("utama").get("footer")
        return "-= {footer} =-".format(
            footer=footer) if footer is not "" else "_" * len(self.header)

    @property
    def header_berhubungan(self):
        return "-= Arti berhubungan dari {ind_utama} =-".format(
                ind_utama=self.dict_obj.get("utama").get("ind"))

    @property
    def body_berhubungan(self):
        arti = []
        arti_berhub = self.dict_obj.get("berhubungan")
        if arti_berhub is not None:
            for berhubungan in arti_berhub:
                a = "{ind} : {ara}".format(
                        ind=berhubungan.get("ind"),
                        ara=berhubungan.get("ara"))
                arti.append(a)

        return "\n".join(arti) if arti else arti

    @property
    def instruction(self):
        result = ['-= Instruksi Layanan Terjemah Angka =-',
                  self.dict_obj.get("instruksi")]
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
        self.dict_ = {'utama': {"ind": "ind_utama",
                                "ara": "ara_utama",
                                "footer": "footer"},
                      'berhubungan': [
                          {"ind": "ind_pertama",
                           "ara": "ara_pertama"},
                          {"ind": "ind_kedua",
                           "ara": "ara_kedua"}
                          ]
                      }
        self.dict_angka = {'utama': {"ind": "1234",
                                     "ara": "ara_utama",
                                     "footer": ""},
                           'instruksi': "Ini adalah instruksi"}

    def test_pretty_output_header(self):
        po = pretty_output(self.dict_).header
        expected = "-= Arti dari ind_utama =-"
        self.assertEqual(po, expected)

    def test_pretty_output_arabic(self):
        po = pretty_output(self.dict_).body
        expected = "ara_utama"
        self.assertEqual(po, expected)

    def test_pretty_output_footer(self):
        po = pretty_output(self.dict_).footer
        expected = "-= footer =-"
        self.assertEqual(po, expected)

    def test_pretty_output_header_berhubungan(self):
        po = pretty_output(self.dict_).header_berhubungan
        expected = "-= Arti berhubungan dari ind_utama =-"
        self.assertEqual(po, expected)

    def test_pretty_output_body_berhubungan(self):
        po = pretty_output(self.dict_).body_berhubungan
        expected = ("ind_pertama : ara_pertama\n"
                    "ind_kedua : ara_kedua")
        self.assertEqual(po, expected)

    def test_pretty_output_hasil(self):
        po = pretty_output(self.dict_).hasil()
        expected = ("-= Arti dari ind_utama =-\n"
                    "ara_utama\n"
                    "-= footer =-\n"
                    "\n"
                    "-= Arti berhubungan dari ind_utama =-\n"
                    "ind_pertama : ara_pertama\n"
                    "ind_kedua : ara_kedua")
        self.assertEqual(po, expected)

    def test_pretty_output_footer_angka(self):
        po = pretty_output(self.dict_angka).footer
        expected = "_" * 20
        self.assertEqual(po, expected)

    def test_pretty_output_hasil_angka(self):
        po = pretty_output(self.dict_angka).hasil()
        expected = ("-= Arti dari 1234 =-\n"
                    "ara_utama\n"
                    "____________________")
        self.assertEqual(po, expected)

    def test_pretty_output_instruction(self):
        po = pretty_output(self.dict_angka).instruction
        expected = ("-= Instruksi Layanan Terjemah Angka =-\n"
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
            result = {"utama": parser.get_arti_master(),
                      "berhubungan": parser.get_all_arti_berhub(
                          self._make_soup)}
            if not pretty:
                return result
            return pretty_output(result).hasil()

        elif layanan == "angka":
            url = self.build_url(query)
            soup = self._make_soup(url)
            parser = AngkaParser(soup)
            result = {"utama": parser.get_arti_master()}
            if not pretty:
                return result
            return pretty_output(result).hasil()

        elif layanan == "angka_instruction":
            url = self.build_url(query)
            soup = self._make_soup(url)
            parser = AngkaParser(soup)
            result = {"instruksi": parser.get_instruction()}
            if not pretty:
                return result
            return pretty_output(result).instruction

    def _make_soup(self, url):
        """Return BeautifulSoup object."""
        resp = requests.get(url)
        return BeautifulSoup(resp.content)

    def build_url(self, query, layanan=None):
        """Return url pencarian sesuai dengan *query* yang dimasukkan."""
        # syntactic sugar
        is_angka = isinstance(query, int) or query.isdigit()

        if not layanan:
            if is_angka:
                url = "http://qaamus.com/terjemah-angka/{number}/angka".format(
                    number=query)
            elif isinstance(query, str):
                query = "+".join(query.split(" "))
                url = "http://qaamus.com/indonesia-arab/{query}/1".format(
                        query=query)
        else:
            if layanan == 'pegon':
                url = 'http://qaamus.com/terjemah-nama/{pegon}'.format(
                    pegon=query)
        return url


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

if __name__ == "__main__":
    unittest.main()
