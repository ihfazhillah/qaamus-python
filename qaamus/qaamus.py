import unittest


class Qaamus:


    def build_idar_url(self, query):
        """adalah fungsi untuk mengganti query spasi dengan + """
        
        query = "+".join(query.split(" "))
        url = "http://qaamus.com/indonesia-arab/" + query + "/1"
        return url

class QaamusTest(unittest.TestCase):


    def test_building_idar_url(self):
        q = Qaamus()
        expected_url = "http://qaamus.com/indonesia-arab/capai/1"
        this_url = q.build_idar_url("capai")
        self.assertEqual(this_url, expected_url)

    def test_building_idar_url_with_multiple_words(self):
        q = Qaamus()
        expected_url = "http://qaamus.com/indonesia-arab/mobil+ambulan+bagus/1"
        this_url = q.build_idar_url("mobil ambulan bagus")
        self.assertEqual(this_url, expected_url)



if __name__ == "__main__":
    unittest.main()
