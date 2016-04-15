import unittest
from bs4 import BeautifulSoup

def get_master(soup):
    result = soup.select("center > .lateef2")
    return result[0]

class QaamusTest(unittest.TestCase):


    def setUp(self):
        with open("/home/sakkuun/Project/qaamus/qaamus-python/html/mobil.html", "rb") as f:
            file = f.read()
        self.soup = BeautifulSoup(file)    
    def test_get_master_tranlated(self):
        master = get_master(self.soup)
        #elf.fail(master) 
        self.assertEqual(master.text, "سيارات")

if __name__ == "__main__":
    unittest.main()
