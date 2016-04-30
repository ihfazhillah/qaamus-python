import unittest
import requests
from bs4 import BeautifulSoup
from ind_ara_parser import IndAraParser


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

    def test_pretty_output_header(self):
        po = pretty_output(self.dict_).header
        expected = "-= Arti dari ind_utama =-"
        self.assertEqual(po, expected)

    def test_pretty_output_arabic(self):
        po = pretty_output(self.dict_).body
        expected = "ara_utama"
        self.assertEqual(po, expected)


class Qaamus:

    def terjemah(self, layanan, query):
        """
        Return terjemahan tergantung dengan **layanan** apa yang dia pilih,
        dan **query** apa yang dia pakai.
        Adapun *layanan* di [Qaamus](qaamus.com) saat ini terdapat 3 layanan:
            * Indonesia Arab
            * Angka
            * Terjemah nama
        Sedangkan *query* adalah query pencarian anda"""
        if layanan == "idar":
            url = self.build_idar_url(query)
            soup = self._make_soup(url)
            parser = IndAraParser(soup)
            return {"utama": parser.get_arti_master(),
                    "berhubungan": parser.get_all_arti_berhub(self._make_soup)}

    def _make_soup(self, url):
        """Return BeautifulSoup object."""
        resp = requests.get(url)
        return BeautifulSoup(resp.content)

    def build_idar_url(self, query):
        """Return url pencarian sesuai dengan *query* yang dimasukkan."""
        query = "+".join(query.split(" "))
        url = "http://qaamus.com/indonesia-arab/{query}/1".format(
                query=query)
        return url


class QaamusTest(unittest.TestCase):

    def test_building_idar_url(self):
        q = Qaamus()
        expected_url = "http://qaamus.com/indonesia-arab/capai/1"
        this_url = q.build_idar_url("capai")
        self.assertEqual(this_url, expected_url)

    def test_building_idar_url_with_multiple_words(self):
        q = Qaamus()
        expected_url = "http://qaamus.com/indonesia-arab/mobil+ambulan+bagus/1"
        this_url = q.build_idar_url("mobil ambulan bagus")
        self.assertEqual(this_url, expected_url)


def idar(query):
    return Qaamus().terjemah("idar", query)

if __name__ == "__main__":
    # print(idar("memukul"))
    unittest.main()
