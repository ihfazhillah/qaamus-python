class QaamusResult(object):
    def __init__(self,
                 ara=None,
                 query=None,
                 footer=None):

        self.ara = ara
        self.query = query
        self.footer = footer

    @property
    def arti_master(self):
        return self.ara, self.query, self.footer

    def __repr__(self):
        retval = "<QaamusResult: {}>".format(self.query)
        return retval


class BaseParser(object):

    def __init__(self, soup):
        """Inisiasi soup objek"""
        self.soup = soup
        self.ara= self.soup.select(
            "center > .lateef2")[0].text.strip()

        # query selectors
        css_select = [".panel-heading > h3 > .label",
                      ".panel-heading > h3 > em"]
        soup = (self.soup.select(x) for x in css_select if self.soup.select(x))
        self.query = next(soup)[0].text

        # footer selector

        try:
            self.footer = self.soup.select(".panel-footer")[0].text
        except IndexError:
            self.footer = None


    def _get_ara(self):
        """Return arti utama."""
        return QaamusResult(ara=self.ara)

    def _get_query(self):
        """Return kata yang dicari."""
        return QaamusResult(query=self.query)

    def _get_footer(self):
        """Return footer pencarian."""
        return QaamusResult(footer=self.footer)

    def get_arti_master(self):
        """
        Return dictionary hasil pencarian dengan kata-kunci
        *ind* untuk pencarian,
        *ara* untuk hasil pencarian,
        *footer* ditampilkan ketika pencarian."""
        return QaamusResult(self.query, self.ara, self.footer)


class InstructionParserMixin(object):
    """Handle getting instrunction."""
    def get_instruction(self):
        text = self.soup.select(".page-header > h1")[0].next_sibling.strip()
        return text


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


class AngkaParser(BaseParser, InstructionParserMixin):
    """Handle terjemah angka page."""
    def get_instruction(self):
        return super(AngkaParser, self).get_instruction(
                                        ).split(",")[1].strip().capitalize()


class PegonParser(BaseParser, InstructionParserMixin):
    """Handle terjemah pegon page."""
