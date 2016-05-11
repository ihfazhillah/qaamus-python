import unittest


class SampleObject(object):
    instruksi = "Ini adalah instruksi"
    query = None
    ara = None
    footer = None
    berhubungan = None


class SampleObjectUtama(object):
    instruksi = None
    query = "coba"
    ara = "coba"
    footer = "Ini footer"
    berhubungan = None


class SampleObjectIdAr(object):
    instruksi = None
    query = "coba"
    ara = "coba"
    footer = "Ini footer"
    berhubungan = [("a", "b"), ("c", "d")]


INSTRUKSI_TEMPLATE = """###
#Instruksi
###

{instruksi}"""


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
            berhubungan = getattr(self.object_, "berhubungan")

            if instruksi:
                return INSTRUKSI_TEMPLATE.format(instruksi=instruksi)

            elif all(utama) and not getattr(self.object_, "berhubungan"):
                template = ("###\n"
                            "#Arti dari {query}\n"
                            "###\n\n"
                            "{ara}\n"

                            "\n{footer}")

                return template.format(
                    query=utama[0],
                    ara=utama[1],
                    footer=utama[2])

            elif all(utama) and berhubungan:
                template = ("###\n"
                            "#Arti dari {query}\n"
                            "###\n\n"
                            "{ara}\n"
                            "\n{footer}"
                            "\n\n"
                            "###\n"
                            "#Arti berhubungan dari {query}\n"
                            "###\n"
                            )
                berhubungan_ = ["%s : %s" % (x[0], x[1]) for x in berhubungan]
                berhubungan = "\n".join(berhubungan_)

                return template.format(
                    query=utama[0],
                    ara=utama[1],
                    footer=utama[2]) + berhubungan


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

    def test_query_ara_footer_with_berhubungan_is_not_none(self):
        view = View(SampleObjectIdAr)
        rendered = view.render()
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
