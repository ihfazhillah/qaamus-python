import os
import unittest
from bs4 import BeautifulSoup

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class IndAraParser:


    def __init__(self, soup):
        self.soup = soup

    def get_ara_master(self):
        result = self.soup.select("center > .lateef2")
        return result[0].text

    def get_ind_master(self):
        result = self.soup.select(".panel-heading > h3 > .label")
        return result[0].text

    def get_footer_master(self):
        result = self.soup.select(".panel-footer")
        return result[0].text

    def get_arti_berhub(self):
        ind = [x.text for x in self.soup.select("td > a")]
        ara = [x.text for x in self.soup.select("td.lateef")]
        result =[{"ind":ind[i], "ara":ara[i]}for i in range(len(ind))] 
        return result

    def get_arti_master(self):
        result = {"ind": self.get_ind_master(),
                  "ara": self.get_ara_master(),
                  "footer": self.get_footer_master()
                 }
        return result

    def get_next_page_url(self):
        #http://stackoverflow.com/questions/9007653/how-to-find-tag-with-particular-text-with-beautiful-soup
        find_next = self.soup.find("a", text="Next »")
        if find_next:
            return find_next['href']
        return False

    def get_all_arti_berhub(self, soupping):
        """
        ini adalah fungsi yang digunakan untuk mendapatkan semua arti berhubungan
        baik dihalaman ini, atau dihalaman yang lainnya
        
        :soup adalah beautifulsoup object
        :soupping adalah fungsi yang digunakan untuk membuat beautifulsoup object
        yang merupakan kombinasi membuka url dan beautifulsoup atau 
        mebuka file dan beautifulsoup
        """
        
        url = self.get_next_page_url()
        result = self.get_arti_berhub()
        while url:
            self.soup = soupping(url)
            url = self.get_next_page_url()
            arti_berhub = self.get_arti_berhub()
            result += arti_berhub
        return result
    


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
        self.assertEqual(secondary[0], {"ind":"rumah sakit gila", "ara":"بَيتُ الـمَجَانِبِينِ، مُسْتَشْفَى الـمَجَانِيْنِ"})
    
    def test_get_arti_master(self):
        "memberikan kembalian berupa dict, {'ind' : indonesia, 'ara': arabic, 'footer': footer_text}"
        master = self.indaraparser.get_arti_master()
        self.assertEqual(master, {"ind":"rumah sakit", "ara":"مستشفى", "footer":"*Diterjemahkan dengan Bing Translator "})
    
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

