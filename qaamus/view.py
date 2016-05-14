import re
from qaamus.utils import default_template


class TemplateParser(object):
    def __init__(self, multiple_line_text):
        self.multiple_line_text = multiple_line_text

    def keys(self):
        """Handle parse keys from multiple lines text."""
        keys = list()
        for index, text in enumerate(self.multiple_line_text):
            match = re.match(r"^####([a-zA-Z0-9_]+)####$", text)
            if match:
                keys.append((match.groups()[0], index))
        return keys

    def result(self):
        """Handle parse values from keys given and return it into
        key-val pair."""
        keys = self.keys()
        result = dict()
        #: looping through whole lists of string for each key
        for idx, key in enumerate(keys):
            key, i_key = key
            values = list()
            for index, text in enumerate(self.multiple_line_text):
                try:
                    #: if text between this key and after : value
                    if keys[idx + 1][1] > index > i_key:
                        values.append(text.strip())
                except IndexError:
                    if index > i_key:
                        values.append(text.strip())
            result[key] = "\n".join(values)
        return result


class View(object):
    """Handle template with object data given."""
    def __init__(self, template_=default_template):
        self.t = template_

    @property
    def template(self):
        with open(self.t, "r") as f:
            multiple_lines = f.readlines()
        return TemplateParser(multiple_lines).result()

    def render(self, object_=None, *args, **kwargs):
        """Handle rendering object into template.

        object is the class with:
            - instruksi : string
            - query : string
            - ara : string
            - footer : string
            - berhubungan : iterable(list,tuple)
        attributes."""
        if object_ is None:
            return "No object found."

        else:
            instruksi = getattr(object_, "instruksi")

            utama = getattr(object_, "utama")
            berhubungan = getattr(object_, "berhubungan")

            # syntactic sugar
            is_instruksi = all([instruksi, not all(utama), not berhubungan])
            is_only_utama = all([utama, not instruksi, not berhubungan])
            is_utama_and_berhubungan = not is_instruksi

            if is_instruksi:
                return self.instruksi_rendered(instruksi, *args, **kwargs)

            elif is_only_utama:
                return self.utama_rendered(utama).strip()

            elif is_utama_and_berhubungan:
                return self.utama_berhubungan_rendered(utama, berhubungan)

    def instruksi_rendered(self, instruksi, layanan=""):
        return self.template['INSTRUKSI_TEMPLATE'].format(instruksi=instruksi,
                                                          layanan=layanan)

    def utama_rendered(self, utama):
        return self.template['UTAMA_TEMPLATE'].format(
            query=utama.query,
            ara=utama.ara,
            footer=utama.footer)

    def utama_berhubungan_rendered(self, utama, berhubungan):
        berhub_header = self.template['BERHUBUNGAN_HEADER_TEMPLATE'].format(
            query=utama.query)

        berhub_body = "\n".join(
            [self.template['BERHUBUNGAN_BODY_TEMPLATE'].format(
                ind=x[0], ara=x[1]) for x in berhubungan])

        return "\n".join([self.utama_rendered(utama),
                          berhub_header,
                          berhub_body])
