import os
import unittest
from bs4 import BeautifulSoup

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_ara_master(soup):
    result = soup.select("center > .lateef2")
    return result[0].text

def get_ind_master(soup):
    result = soup.select(".panel-heading > h3 > .label")
    return result[0].text

def get_footer_master(soup):
    result = soup.select(".panel-footer")
    return result[0].text

def get_arti_berhub(soup):
    ind = [x.text for x in soup.select("td > a")]
    ara = [x.text for x in soup.select("td.lateef")]
    result =[{"ind":ind[i], "ara":ara[i]}for i in range(len(ind))] 
    return result

def get_arti_master(soup):
    result = {"ind": get_ind_master(soup),
              "ara": get_ara_master(soup),
              "footer": get_footer_master(soup)
             }
    return result

def get_next_page_url(soup):
    #http://stackoverflow.com/questions/9007653/how-to-find-tag-with-particular-text-with-beautiful-soup
    find_next = soup.find("a", text="Next »")
    if find_next:
        return find_next['href']
    return False

def get_all_arti_berhub(soup, soupping):
    """
    ini adalah fungsi yang digunakan untuk mendapatkan semua arti berhubungan
    baik dihalaman ini, atau dihalaman yang lainnya
    
    :soup adalah beautifulsoup object
    :soupping adalah fungsi yang digunakan untuk membuat beautifulsoup object
    yang merupakan kombinasi membuka url dan beautifulsoup atau 
    mebuka file dan beautifulsoup
    """
    
    #Dapatkan all url dahulu
    urls = []
    url_to_visit = []
    url = get_next_page_url(soup)
    result = get_arti_berhub(soup)
    while url:
        urls.append(url)
        url_to_visit.append(url)
        soup = soupping(urls[0])
        urls.pop()
        url = get_next_page_url(soup)
        arti_berhub = get_arti_berhub(soup)
        result = result + arti_berhub
    return result
    


class AraIndParserTest(unittest.TestCase):


    def get_abs_path(self, path):
        return os.path.join(BASE_DIR, path)

    def soupping(self, file):
        with open(file, 'rb') as f:
            file = f.read()
        return BeautifulSoup(file)

    def setUp(self):
        self.soup = self.soupping(self.get_abs_path('html/mobil.html'))
    
    def test_get_master_tranlated(self):
        master = get_ara_master(self.soup)
        self.assertEqual(master, "سيارات")

    def test_get_master_ind(self):
        master = get_ind_master(self.soup)
        self.assertEqual(master, "mobil")

    def test_get_footer_translation(self):
        master = get_footer_master(self.soup)
        self.assertEqual(master, "*Diterjemahkan dengan Bing Translator ")

    def test_get_arti_berhub_jumlah(self):
        secondary = get_arti_berhub(self.soup)
        self.assertEqual(len(secondary), 10)

    def test_get_arti_berhub_first(self):
        secondary = get_arti_berhub(self.soup)
        self.assertEqual(secondary[0], {"ind":"bak persneleng (mobil)", "ara":"صُنْدُوقُ السُّرْعَةِ"})
    
    def test_get_arti_master(self):
        "memberikan kembalian berupa dict, {'ind' : indonesia, 'ara': arabic, 'footer': footer_text}"
        master = get_arti_master(self.soup)
        self.assertEqual(master, {"ind":"mobil", "ara":"سيارات", "footer":"*Diterjemahkan dengan Bing Translator "})
    
    def test_get_next_page_url(self):
        url_to = get_next_page_url(self.soup)
        self.assertEqual(url_to, self.get_abs_path("html/mobil2.html"))

    def test_get_next_page_url_with_no_next_in_page(self):
        soup = self.soupping(self.get_abs_path("html/mobil2.html"))
        no_next = get_next_page_url(soup)
        self.assertFalse(no_next)

    def test_get_all_kata_berhub(self):
        secondary = get_all_arti_berhub(self.soup, self.soupping)
        self.assertEqual(len(secondary), 16)


if __name__ == "__main__":
    unittest.main()

