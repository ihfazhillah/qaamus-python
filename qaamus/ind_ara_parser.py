from bs4 import BeautifulSoup


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
    

