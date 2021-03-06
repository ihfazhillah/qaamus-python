import unittest
from qaamus.out import Result


class ResultTestCase(unittest.TestCase):

    def test_result_with_none_input(self):
        result = Result()
        self.assertEqual(result.query, None)
        self.assertEqual(result.ara, None)
        self.assertEqual(result.footer, None)

    def test_result_with_result_input(self):
        """query, ara, footer object."""
        result = Result("ind_utama", "ara_utama", "footer")
        self.assertEqual(result.query, "ind_utama")
        self.assertEqual(result.ara, "ara_utama")
        self.assertEqual(result.footer, "footer")

    def test_get_return_tuple(self):
        result = Result("ind_utama", "ara_utama", "footer")
        expected = ("ind_utama", "ara_utama", "footer")
        self.assertEqual(result.utama, expected)

    def test_result_with_result_input_berhubungan(self):
        result = Result(berhubungan=[(1, 2), (3, 4)])
        expected = [(1, 2), (3, 4)]
        self.assertEqual(result.berhubungan, expected)

    def test_result_with_result_input_berhubungan_generator_obj(self):
        result = Result(berhubungan=(x for x in range(4)))
        expected = [0, 1, 2, 3]
        self.assertEqual(result.berhubungan, expected)

    def test_result_with_instruction_arg(self):
        result = Result(instruksi="Ini adalah instruksi")
        expected = 'Ini adalah instruksi'
        self.assertEqual(result.instruksi, expected)
