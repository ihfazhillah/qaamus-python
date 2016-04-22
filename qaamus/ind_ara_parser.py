from bs4 import BeautifulSoup


class IndAraParser(object):
    """Class untuk parsing halaman terjemah 
    indonesia arab."""

    def __init__(self, soup):
        """Inisiasi soup objek"""
        self.soup = soup

    def _get_ara_master(self):
        """Return arti utama."""
        return self.soup.select("center > .lateef2")[0].text

    def _get_ind_master(self):
        """Return kata yang dicari."""
        return self.soup.select(".panel-heading > h3 > .label")[0].text

    def _get_footer_master(self):
        """Return footer pencarian, bisa jadi pencarian menggunakan
        Bing translator sehingga ditampilkan di web."""
        return self.soup.select(".panel-footer")[0].text
    
    def get_arti_master(self):
        """Return dictionary hasil pencarian dengan kata-kunci 
        *ind* untuk pencarian,
        *ara* untuk hasil pencarian,
        *footer* ditampilkan ketika pencarian menggunakan Bing translator."""
        return {"ind": self._get_ind_master(),
                "ara": self._get_ara_master(),
                "footer": self._get_footer_master()
               }

    def get_arti_berhub(self, soup=None):
        """Return list of dictionary berupa arti berhubungan
        dengan arti utama dengan **kata-kunci**
        *ind* adalah indonesia
        *ara* adalah arti arabnya."""
        if soup is None:
            soup = self.soup

        ind = [x.text for x in soup.select("td > a")]
        ara = [x.text for x in soup.select("td.lateef")]
        return [{"ind":ind[i], "ara":ara[i]}for i in range(len(ind))] 

    def get_next_page_url(self):
        """Return url next page bila program menemukan *Next »*,
        else: return *False*."""
        #http://stackoverflow.com/questions/9007653/how-to-find-tag-with-particular-text-with-beautiful-soup
        find_next = self.soup.find("a", text="Next »")
        if find_next:
            return find_next['href']
        return False

    def get_all_arti_berhub(self, make_soup):
        """
        ini adalah fungsi yang digunakan untuk mendapatkan semua arti berhubungan
        baik dihalaman ini, atau dihalaman yang lainnya
        
        :make_soup adalah fungsi yang digunakan untuk membuat beautifulsoup object
        yang merupakan kombinasi membuka url dan beautifulsoup atau 
        mebuka file dan beautifulsoup
        """
        
        url = self.get_next_page_url()
        result = self.get_arti_berhub()
        while url:
            soup = make_soup(url)
            url = self.get_next_page_url()
            result += self.get_arti_berhub(soup)
        return result
    
