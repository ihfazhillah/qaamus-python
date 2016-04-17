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

def get_next_page_url(url, condition):
    """
    Fungsi untuk mendapatkan url next page ketika kondisi 
    == True
    Fungsi ini khusus (yang saya tahu sekarang) qaamus.com
    dikarenakan website ini berformat
    http://qaamus.com/indonesia-arab/mobil/1 <-- untuk hal pertama
    http://qaamus.com/indonesia-arab/mobil/2 <-- untuk hal kedua

    :url adalah url semula
    :condition adalah sebuah kondisi dimana harus True
    """

    if condition :
        splitted_url = url.split("/")
        page_number = splitted_url[-1]
        next_page_number = int(page_number) + 1
        splitted_url.pop()
        splitted_url.append(str(next_page_number))
        return "/".join(splitted_url)
    return "Nothing to do."


class AraIndParserTest(unittest.TestCase):


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
    
    def test_get_next_page_url(self):
        url = "http://qaamus.com/indonesia-arab/mobil/1"
        url_to = get_next_page_url(url, True)
        self.assertEqual(url_to, "http://qaamus.com/indonesia-arab/mobil/2")

    def test_get_next_page_url_with_false_condition_return_nothing_to_do(self):
        url = "http://qaamus.com/indonesia-arab/mobil/2"
        nothing_to_do = get_next_page_url(url, False)
        self.assertEqual(nothing_to_do, "Nothing to do.")
if __name__ == "__main__":
    unittest.main()

