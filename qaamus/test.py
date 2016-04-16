import unittest
from bs4 import BeautifulSoup

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
    arti = soup.select("td > a")
    arti = [ x.text for x in arti ] 
    ara = soup.select("td.lateef")
    ara = [x.text for x in ara]
    result = zip(arti, ara) 
    return list(result)

class QaamusTest(unittest.TestCase):


    def setUp(self):
        with open("/home/sakkuun/Project/qaamus/qaamus-python/html/mobil.html", "rb") as f:
            file = f.read()
        self.soup = BeautifulSoup(file)    
    
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
        self.assertEqual(secondary[0], ("bak persneleng (mobil)", "صُنْدُوقُ السُّرْعَةِ"))

if __name__ == "__main__":
    unittest.main()
