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
    ind = [x.text for x in soup.select("td > a")]
    ara = [x.text for x in soup.select("td.lateef")]
    result = []
    for i in range(len(ind)):
       result.append({"ind":ind[i], "ara":ara[i]})
    return result

def get_arti_master(soup):
    result = {"ind": get_ind_master(soup),
              "ara": get_ara_master(soup),
              "footer": get_footer_master(soup)
             }
    return result

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
        self.assertEqual(secondary[0], {"ind":"bak persneleng (mobil)", "ara":"صُنْدُوقُ السُّرْعَةِ"})
    
    def test_get_arti_master(self):
        "memberikan kembalian berupa dict, {'ind' : indonesia, 'ara': arabic, 'footer': footer_text}"
        master = get_arti_master(self.soup)
        self.assertEqual(master, {"ind":"mobil", "ara":"سيارات", "footer":"*Diterjemahkan dengan Bing Translator "})

if __name__ == "__main__":
    unittest.main()
