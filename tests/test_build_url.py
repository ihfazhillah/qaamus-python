import unittest
from qaamus.utils import build_url, LayananValueError


class BuildUrlTest(unittest.TestCase):

    def test_building_idar_url(self):
        expected_url = "http://qaamus.com/indonesia-arab/capai/1"
        this_url = build_url("capai")
        self.assertEqual(this_url, expected_url)

    def test_building_idar_url_with_multiple_words(self):
        expected_url = "http://qaamus.com/indonesia-arab/mobil+ambulan+bagus/1"
        this_url = build_url("mobil ambulan bagus")
        self.assertEqual(this_url, expected_url)

    def test_building_angka_url(self):
        expected_url = "http://qaamus.com/terjemah-angka/123/angka"
        this_url = build_url("123")
        self.assertEqual(this_url, expected_url)

    def test_building_pegon_url(self):
        expected_url = "http://qaamus.com/terjemah-nama/suratman"
        this_url = build_url("suratman", "pegon")
        self.assertEqual(this_url, expected_url)

    def test_building_angka_url_with_layanan(self):
        expected_url = "http://qaamus.com/terjemah-angka/123/angka"
        this_url = build_url("123", 'angka')
        self.assertEqual(this_url, expected_url)

    def test_building_idar_url_with_multiple_words_with_layanan(self):
        expected_url = "http://qaamus.com/indonesia-arab/mobil+ambulan+bagus/1"
        this_url = build_url("mobil ambulan bagus", 'idar')
        self.assertEqual(this_url, expected_url)

    def test_building_idar_url_with_layanan(self):
        expected_url = "http://qaamus.com/indonesia-arab/capai/1"
        this_url = build_url("capai", 'idar')
        self.assertEqual(this_url, expected_url)

    def test_building_url_with_wrong_layanan(self):
        try:
            build_url("capai", "lainnya")
        except LayananValueError as L:
            self.assertEqual(L.message, "Layanan tidak ditemukan")


if __name__ == "__main__":
    unittest.main()
