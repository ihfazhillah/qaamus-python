import os
from bs4 import BeautifulSoup


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def soupping(file):
    with open(file, 'rb') as f:
        file = f.read()
    return BeautifulSoup(file)


def get_abs_path(path):
    return os.path.join(BASE_DIR, path)


idar_soup = soupping(get_abs_path("html/rumah+sakit"))
angka_soup = soupping(get_abs_path("html/angka123"))
pegon_soup = soupping(get_abs_path("html/pegon_suratman"))
