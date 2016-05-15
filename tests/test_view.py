import unittest
from qaamus.view import View, TemplateParser
from qaamus.utils import default_template
from collections import namedtuple


utama = namedtuple("utama", ("query", "ara", "footer"))


class SampleObject(object):
    instruksi = "Ini adalah instruksi"
    query = None
    ara = None
    footer = None
    berhubungan = None
    utama = utama(query, ara, footer)


class SampleObjectUtama(object):
    instruksi = None
    query = "coba"
    ara = "coba"
    footer = "Ini footer"
    berhubungan = None
    utama = utama(query, ara, footer)


class SampleObjectIdAr(object):
    instruksi = None
    query = "coba"
    ara = "coba"
    footer = "Ini footer"
    berhubungan = [("a", "b"), ("c", "d")]
    utama = utama(query, ara, footer)


class ViewTestCase(unittest.TestCase):
    def test_empty_template(self):
        view = View()
        rendered = view.render()
        self.assertEqual(rendered, "No object found.")

    def test_empty_object(self):
        view = View(default_template)
        rendered = view.render()
        self.assertEqual(rendered, "No object found.")

    def test_only_instruction_is_not_none(self):
        view = View(default_template)
        rendered = view.render(SampleObject, "Angka")
        self.assertEqual(rendered,
                         "###\n#Instruksi Layanan Angka\n###"
                         "\n\nIni adalah instruksi")

    def test_query_ara_footer_is_not_none(self):
        view = View(default_template)
        rendered = view.render(SampleObjectUtama)
        expected = ("###\n"
                    "#Arti dari coba\n"
                    "###\n\n"
                    "coba\n"
                    "\nIni footer")
        self.assertEqual(rendered, expected)

    def test_query_ara_footer_with_berhubungan_is_not_none(self):
        view = View(default_template)

        rendered = view.render(SampleObjectIdAr)
        expected = ("###\n"
                    "#Arti dari coba\n"
                    "###\n\n"
                    "coba\n"
                    "\nIni footer"
                    "\n\n"
                    "###\n"
                    "#Arti berhubungan dari coba\n"
                    "###\n"
                    "a : b\n"
                    "c : d")
        self.assertEqual(rendered, expected)
if __name__ == "__main__":
    unittest.main()
