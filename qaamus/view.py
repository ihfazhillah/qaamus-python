import unittest


class View(object):
    def render(self):
        return "No object found."


class ViewTestCase(unittest.TestCase):
    def test_empty_object(self):
        view = View()
        rendered = view.render()
        self.assertEqual(rendered, "No object found.")


if __name__ == "__main__":
    unittest.main()
