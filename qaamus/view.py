import unittest


class SampleObject(object):
    instruksi = "Ini adalah instruksi"


class View(object):
    def __init__(self, object_=None):
        self.object_ = object_

    def render(self):
        if self.object_ is None:
            return "No object found."
        else:
            if hasattr(self.object_, "instruksi"):
                instruksi = getattr(self.object_, "instruksi")
                header = ("###\n"
                          "#Instruksi\n"
                          "###\n")
                return "\n".join([header, instruksi])


class ViewTestCase(unittest.TestCase):
    def test_empty_object(self):
        view = View()
        rendered = view.render()
        self.assertEqual(rendered, "No object found.")

    def test_only_instruction_is_not_none(self):
        view = View(SampleObject)
        rendered = view.render()
        self.assertEqual(rendered, "###\n#Instruksi\n###\n\nIni adalah instruksi")


if __name__ == "__main__":
    unittest.main()
