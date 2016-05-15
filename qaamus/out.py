from collections import namedtuple


utama = namedtuple("utama", ("query", "ara", "footer"))


class Result(object):
    def __init__(self,
                 query=None,
                 ara=None,
                 footer=None,
                 berhubungan=None,
                 instruksi=None):
        self.query = query
        self.ara = ara
        self.footer = footer
        self.instruksi = instruksi
        self._berhubungan = berhubungan
        self.utama = utama(self.query, self.ara, self.footer)

    @property
    def berhubungan(self):
        if hasattr(self._berhubungan, "__iter__"):
            return list(self._berhubungan)
        return self._berhubungan
