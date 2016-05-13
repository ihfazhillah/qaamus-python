import view
import parsers

def idar_controller(soup_object, make_soup):
    data = parsers.IndAraParser(soup_object).get_idar(make_soup)
    rendered = view.View().render(data)
    return rendered

def angka_controller(soup_object):
    data = parsers.AngkaParser(soup_object).get_arti_master()
    rendered = view.View().render(data)
    return rendered

def pegon_controller(soup_object):
    data = parsers.AngkaParser(soup_object).get_arti_master()
    rendered = view.View().render(data)
    return rendered

def angka_instruksi_controller(soup_object):
    data = parsers.AngkaParser(soup_object).get_instruction()
    rendered = view.View().render(data, layanan="Angka")
    return rendered

def pegon_instruksi_controller(soup_object):
    data = parsers.AngkaParser(soup_object).get_instruction()
    rendered = view.View().render(data, layanan="Pegon")
    return rendered

import unittest
from test_parsers import soupping, get_abs_path


idar_soup = soupping(get_abs_path("html/rumah+sakit"))
angka_soup = soupping(get_abs_path("html/angka123"))
pegon_soup = soupping(get_abs_path("html/pegon_suratman"))


class ControllerTestCase(unittest.TestCase):

    def test_idar_controller(self):
        result = idar_controller(idar_soup, soupping)
        self.assertTrue(isinstance(result, str))
        self.assertTrue(result is not None)

    def test_angka_controller(self):
        result = angka_controller(angka_soup)
        self.assertTrue(isinstance(result, str))
        self.assertTrue(result is not None)

    def test_pegon_controller(self):
        result = pegon_controller(pegon_soup)
        self.assertTrue(isinstance(result, str))
        self.assertTrue(result is not None)

    def test_angka_instruksi_controller(self):
        result = angka_instruksi_controller(angka_soup)
        self.assertIn("Instruksi Layanan Angka", result)

    def test_pegon_instruksi_controller(self):
        result = pegon_instruksi_controller(angka_soup)
        self.assertIn("Instruksi Layanan Pegon", result)


if __name__ == "__main__":
    unittest.main()
