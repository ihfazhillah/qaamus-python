import os
import requests
from bs4 import BeautifulSoup


#: exceptions
class LayananValueError(ValueError):
    def __init__(self, message=None):
        super(LayananValueError, self).__init__(message)
        self.message = message


#: dirs
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def soupping(file):
    if file.startswith("http"):
        resp = requests.get(file)
        file = resp.content
    else:
        with open(file, 'rb') as f:
            file = f.read()
    return BeautifulSoup(file)


def get_abs_path(path):
    return os.path.join(BASE_DIR, path)

default_template = get_abs_path("qaamus/default_template")


def build_url(query, layanan=None):
    """Return url pencarian sesuai dengan *query* yang dimasukkan.
    layanan ketika None maka akan terjadi pengecekan query,
    kalau query adalah integer atau seperti integer maka berikan kembalian
    ANGKA_URL,
    kalau string maka secara default akan direfrensikan ke INDO_URL.
    Bila tidak None, maka tergantung dengan layanan yang diminta."""

    # syntactic sugar
    is_angka = isinstance(query, int) or query.isdigit()

    ANGKA_URL = "http://qaamus.com/terjemah-angka/{number}/angka".format(
        number=query)
    INDO_URL = "http://qaamus.com/indonesia-arab/{query}/1".format(
        query="+".join(query.split()))
    PEGON_URL = 'http://qaamus.com/terjemah-nama/{pegon}'.format(
        pegon=query)

    layanan_mapping = dict(
        (('angka', ANGKA_URL),
            ('idar', INDO_URL),
            ('pegon', PEGON_URL))
        )

    if not layanan:
        if is_angka:
            url = ANGKA_URL
        elif isinstance(query, str):
            url = INDO_URL
    else:
        if layanan in layanan_mapping:
            url = layanan_mapping[layanan]
        else:
            raise LayananValueError("Layanan tidak ditemukan")

    return url
