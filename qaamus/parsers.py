import re
from collections import namedtuple
from qaamus.out import Result


class BaseParser(object):

    def __init__(self, soup):
        """Inisiasi soup objek"""
        self.soup = soup

    def _get_ara(self):
        """Return arti utama."""
        return self.soup.select("center > .lateef2")[0].text.strip()

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
        return Result(self._get_query(),
                      self._get_ara(),
                      self._get_footer())


class InstructionParserMixin(object):
    """Handle getting instrunction."""
    def get_instruction(self):
        text = self.soup.select(".page-header > h1")[0].next_sibling.strip()
        return Result(instruksi=text)


class IndAraParser(BaseParser):
    """Class untuk parsing halaman terjemah
    indonesia arab."""

    def get_arti_berhub(self, soup=None):
        self.soup = soup or self.soup

        ind = [x.text for x in self.soup.select("td > a")]
        ara = [x.text for x in self.soup.select("td.lateef")]
        return Result(berhubungan=zip(ind, ara))

    def get_next_page_url(self):
        """Return url next page bila program menemukan *Next »*,
        else: return *False*."""
        # http://stackoverflow.com/questions/9007653/how-to-find-tag-with-particular-text-with-beautiful-soup
        find_next = self.soup.find("a", text="Next »")
        return find_next['href'] if find_next else False

    def get_all_arti_berhub(self, make_soup):
        url = self.get_next_page_url()
        result = self.get_arti_berhub().berhubungan
        while url:
            next_soup = make_soup(url)
            next_page = self.get_arti_berhub(next_soup).berhubungan
            result += next_page
            url = self.get_next_page_url()
        return Result(berhubungan=result)

    def get_idar(self, make_soup):
        utama = self.get_arti_master()
        berhubungan = self.get_all_arti_berhub(make_soup)
        return Result(query=utama.query,
                      ara=utama.ara,
                      footer=utama.footer,
                      berhubungan=berhubungan.berhubungan)


class AngkaParser(BaseParser, InstructionParserMixin):
    """Handle terjemah angka page."""
    def get_instruction(self):
        text = super(AngkaParser, self).get_instruction().instruksi
        return Result(instruksi=text.split(",")[1].strip().capitalize())


class PegonParser(BaseParser, InstructionParserMixin):
    """Handle terjemah pegon page."""


class TemplateParser(object):
    def __init__(self, multiple_line_text):
        self.multiple_line_text = multiple_line_text

    def keys(self, var_re=None):
        """Handle parse keys from multiple lines text.

        optional: var_re
        kalau tidak di beri, maka secara default akan mencari text
        yang berada ditengah #### ####. Dengan karakter yang diijinkan
        huruf besar, kecil, angka dan underscore."""

        var_re = var_re or re.compile(r"^####([a-zA-Z0-9_]+)####$")
        keys = list()
        for index, text in enumerate(self.multiple_line_text):
            match = re.match(var_re, text)
            if match:
                keys.append((match.groups()[0], index))
        return keys

    def result(self):
        """Handle parse values from keys given and return it into
        key-val pair."""
        keys = self.keys()
        result = dict()
        #: looping through whole lists of string for each key
        for idx, key in enumerate(keys):
            key, i_key = key
            values = list()
            for index, text in enumerate(self.multiple_line_text):
                try:
                    #: if text between this key and after : value
                    if keys[idx + 1][1] > index > i_key:
                        values.append(text.strip())
                except IndexError:
                    if index > i_key:
                        values.append(text.strip())
            result[key] = "\n".join(values)
        return namedtuple("Template", result.keys())(**result)
