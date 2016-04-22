import unittest
import requests
from bs4 import BeautifulSoup
from ind_ara_parser import IndAraParser

class Qaamus:


    def terjemah(self, layanan, query):
        if layanan == "idar":
            url = self.build_idar_url(query)
            soup = self._make_soup(url)
            parser = IndAraParser(soup)
            return {"utama" : parser.get_arti_master(),
                    "berhubungan" : parser.get_all_arti_berhub(self._make_soup)
                   }



    def _make_soup(self, url):
        """Return BeautifulSoup object."""
        resp = requests.get(url)
        return BeautifulSoup(resp.content)

    def build_idar_url(self, query):
        """Return url pencarian sesuai dengan *query* yang dimasukkan.""" 
        query = "+".join(query.split(" "))
        url = "http://qaamus.com/indonesia-arab/" + query + "/1"
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



if __name__ == "__main__":
    q = Qaamus()
    print(q.terjemah("idar", "memukul"))
    unittest.main()
