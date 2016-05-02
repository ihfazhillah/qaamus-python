class BaseParser(object):

    def __init__(self, soup):
        """Inisiasi soup objek"""
        self.soup = soup

    def _get_ara(self):
        """Return arti utama."""
        return self.soup.select("center > .lateef2")[0].text

    def _get_query(self):
        """Return kata yang dicari."""
        css_select = [".panel-heading > h3 > .label",
                      ".panel-heading > h3 > em"]
        soup = (self.soup.select(x) for x in css_select if self.soup.select(x))
        result = next(soup)[0].text
        return result

    def _get_footer(self):
        """Return footer pencarian."""
        try:
            return self.soup.select(".panel-footer")[0].text
        except IndexError:
            return ''

    def get_arti_master(self):
        """
        Return dictionary hasil pencarian dengan kata-kunci
        *ind* untuk pencarian,
        *ara* untuk hasil pencarian,
        *footer* ditampilkan ketika pencarian."""
        return {"ind": self._get_query(),
                "ara": self._get_ara(),
                "footer": self._get_footer()}


class IndAraParser(BaseParser):
    """Class untuk parsing halaman terjemah
    indonesia arab."""

    def get_arti_berhub(self, soup=None):
        """Return list of dictionary berupa arti berhubungan
        dengan arti utama dengan **kata-kunci**
        *ind* adalah indonesia
        *ara* adalah arti arabnya."""
        if soup is not None:
            self.soup = soup

        ind = [x.text for x in self.soup.select("td > a")]
        ara = [x.text for x in self.soup.select("td.lateef")]
        return [{"ind": ind[i], "ara":ara[i]}for i in range(len(ind))]

    def get_next_page_url(self):
        """Return url next page bila program menemukan *Next »*,
        else: return *False*."""
        # http://stackoverflow.com/questions/9007653/how-to-find-tag-with-particular-text-with-beautiful-soup
        find_next = self.soup.find("a", text="Next »")
        if find_next:
            return find_next['href']
        return False

    def get_all_arti_berhub(self, make_soup):
        """
        ini adalah fungsi yang digunakan untuk mendapatkan semua arti
        berhubungan baik dihalaman ini, atau dihalaman yang lainnya

        :make_soup adalah fungsi yang digunakan untuk membuat beautifulsoup
        object yang merupakan kombinasi membuka url dan beautifulsoup atau
        mebuka file dan beautifulsoup
        """
        url = self.get_next_page_url()
        result = self.get_arti_berhub()
        while url:
            next_soup = make_soup(url)
            next_page = self.get_arti_berhub(next_soup)
            result += next_page
            url = self.get_next_page_url()
        return result


class AngkaParser(BaseParser):
    """Handle terjemah angka page."""
    def get_instruction(self):
        """Return the instruction text.

        text is returning 'Terjemah angka adalah menterjemahkan angka
        kedalam bahasa arab, caranya cukup mudah ketik angka
        (tanpa titik dan koma) yang akan di terjemahkan'."""
        text = self.soup.select(".page-header > h1")[0].next_sibling.strip()
        return text.split(",")[1].strip().capitalize()
