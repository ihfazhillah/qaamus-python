from qaamus.utils import default_template
from .parsers import TemplateParser


class View(object):
    """Handle template with object data given."""
    def __init__(self, template_file=default_template):
        self.t = template_file

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
        return self.template.INSTRUKSI_TEMPLATE.format(instruksi=instruksi,
                                                       layanan=layanan)

    def utama_rendered(self, utama):
        return self.template.UTAMA_TEMPLATE.format(
            query=utama.query,
            ara=utama.ara,
            footer=utama.footer)

    def utama_berhubungan_rendered(self, utama, berhubungan):
        berhub_header = self.template.BERHUBUNGAN_HEADER_TEMPLATE.format(
            query=utama.query)

        berhub_body = "\n".join(
            [self.template.BERHUBUNGAN_BODY_TEMPLATE.format(
                ind=x[0], ara=x[1]) for x in berhubungan])

        return "\n".join([self.utama_rendered(utama),
                          berhub_header,
                          berhub_body])
