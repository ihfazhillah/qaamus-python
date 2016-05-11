
class View(object):
    """Handle template with object data given."""
    def __init__(self, template_="default_template"):
        """Handle importing template."""
        self.template = __import__(template_)

    def render(self, object_=None):
        """Handle rendering object into template.

        object is the class with:
            - instruksi : string
            - query : string
            - ara : string
            - footer : string
            - berhubungan : iterable(list,tuple)
        attributes."""
        template = self.template

        if object_ is None:
            return "No object found."

        else:
            instruksi = getattr(object_, "instruksi")
            utama = [getattr(object_, x)
                     for x in ["query", "ara", "footer"]]
            berhubungan = getattr(object_, "berhubungan")

            # syntactic sugar
            is_instruksi = all([instruksi, not all(utama), not berhubungan])
            is_only_utama = all([utama, not instruksi, not berhubungan])
            is_utama_and_berhubungan = not is_instruksi

            if is_instruksi:
                return template.INSTRUKSI_TEMPLATE.format(instruksi=instruksi)

            elif is_only_utama:
                return template.UTAMA_TEMPLATE.format(
                    query=utama[0],
                    ara=utama[1],
                    footer=utama[2])

            elif is_utama_and_berhubungan:
                utama_ = template.UTAMA_TEMPLATE.format(query=utama[0],
                                                        ara=utama[1],
                                                        footer=utama[2])
                berhub_header = template.BERHUBUNGAN_HEADER_TEMPLATE.format(
                    query=utama[0])
                berhub_body = "\n".join(
                    [template.BERHUBUNGAN_BODY_TEMPLATE.format(ind=x[0],
                                                               ara=x[1])
                     for x in berhubungan]
                )
                return "\n".join([utama_, berhub_header, berhub_body])
