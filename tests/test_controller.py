import unittest
from qaamus.utils import (soupping,
                          idar_soup,
                          angka_soup,
                          pegon_soup)
from qaamus.controller import (idar_controller,
                               angka_controller,
                               pegon_controller,
                               angka_instruksi_controller,
                               pegon_instruksi_controller)


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
