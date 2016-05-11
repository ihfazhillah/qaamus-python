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

UTAMA_TEMPLATE = """###
#Arti dari {query}
###

{ara}

{footer}"""

BERHUBUNGAN_HEADER_TEMPLATE = """
###
#Arti berhubungan dari {query}
###"""

BERHUBUNGAN_BODY_TEMPLATE = """{ind} : {ara}"""


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

            # syntactic sugar
            is_instruksi = all([instruksi, not all(utama), not berhubungan])
            is_only_utama = all([utama, not instruksi, not berhubungan])
            is_utama_and_berhubungan = not is_instruksi

            if is_instruksi:
                return INSTRUKSI_TEMPLATE.format(instruksi=instruksi)

            elif is_only_utama:
                return UTAMA_TEMPLATE.format(
                    query=utama[0],
                    ara=utama[1],
                    footer=utama[2])

            elif is_utama_and_berhubungan:
                utama_ = UTAMA_TEMPLATE.format(query=utama[0],
                                              ara=utama[1],
                                              footer=utama[2])
                berhub_header = BERHUBUNGAN_HEADER_TEMPLATE.format(
                    query=utama[0])
                berhub_body = "\n".join([BERHUBUNGAN_BODY_TEMPLATE.format(
                                                                 ind=x[0],
                                                                 ara=x[1])
                                          for x in berhubungan])
                return "\n".join([utama_, berhub_header, berhub_body])


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
