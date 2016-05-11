import unittest


class SampleObject(object):
    instruksi = "Ini adalah instruksi"
    query = None
    ara = None
    footer = None


class SampleObjectUtama(object):
    instruksi = None
    query = "coba"
    ara = "coba"
    footer = "Ini footer"


class View(object):
    def __init__(self, object_=None):
        self.object_ = object_

    def render(self):
        if self.object_ is None:
            return "No object found."
        else:
            instruksi = getattr(self.object_, "instruksi")
            utama = [getattr(self.object_, x) for x in
                     ["query", "ara", "footer"]]
            if instruksi:
                header = ("###\n"
                          "#Instruksi\n"
                          "###\n")
                return "\n".join([header, instruksi])
            elif all(utama):
                template = ("###\n"
                            "#Arti dari {query}\n"
                            "###\n\n"
                            "{ara}\n"

                            "\n{footer}")

                return template.format(
                    query=utama[0],
                    ara=utama[1],
                    footer=utama[2])


class ViewTestCase(unittest.TestCase):
    def test_empty_object(self):
        view = View()
        rendered = view.render()
        self.assertEqual(rendered, "No object found.")

    def test_only_instruction_is_not_none(self):
        view = View(SampleObject)
        rendered = view.render()
        self.assertEqual(rendered,
                         "###\n#Instruksi\n###\n\nIni adalah instruksi")

    def test_query_ara_footer_is_not_none(self):
        view = View(SampleObjectUtama)
        rendered = view.render()
        expected = ("###\n"
                    "#Arti dari coba\n"
                    "###\n\n"
                    "coba\n"
                    "\nIni footer")
        self.assertEqual(rendered, expected)


if __name__ == "__main__":
    unittest.main()
