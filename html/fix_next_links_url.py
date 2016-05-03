import os
import re
import unittest
from bs4 import BeautifulSoup


THIS_DIR = os.path.abspath(os.path.dirname("__file__"))


def increase_file_name(file_path):
    """Return file_name with increased file_name from *file_path*."""
    dir_path, file_name = os.path.split(file_path)
    num = re.match(r'.*?(\d+)$', file_name)
    num = num.group(1) if num else ''
    if num.isdigit():
        new_file_name = file_name.replace(num, str(int(num) + 1))
    else:
        new_file_name = file_name + "2"
    return os.path.join(dir_path, new_file_name)


def make_soup(path):
    """Return BeautifulSoup object."""
    if not os.path.isdir(path):
        with open(path, "rb") as f:
            return BeautifulSoup(f)


def get_next_path(soup):
    """Return <a> tag with 'Next \xbb' text.
    False if not found."""
    path = soup.find("a", text="Next »")
    if path:
        return path
    return False


def replace_path(path, new_path=None):
    """Return replaced <a> soup object with *new_path*.
    *path* is a <a> soup object returned by make_soup func."""
    if new_path is not None:
        path['href'] = new_path
    else:
        path = path
    return path['href']


def save_replaced(soup, path):
    """Save *soup* object into a file  with *path* as filename."""
    with open(path, "w") as f:
        f.write(str(soup))


def replace(file_path, new_file_path):
    """Replace href attr with 'Next \xbb' text into  *new_file_path* given
    by user from *file_path*."""
    print()
    print(">>>initializing soup object from {file}".format(file=file_path))
    soup = make_soup(file_path)
    print()
    print(">>>getting next url....")
    next_path_old = get_next_path(soup)
    if next_path_old:
        print(">>>Next url found : {next_url}".format(
            next_url=next_path_old['href']))
        print(">>>Replacing {next_url} with {file_path}".format(
            next_url=next_path_old['href'],
            file_path=new_file_path))
        replace_path(next_path_old, new_file_path)
    else:
        print(">>>No next url in {file_path}".format(file_path=file_path))
        print(">>>Saving {file} file".format(file=file_path))
    save_replaced(soup, file_path)
    print()
    print(">>>Done")


class FixNextUrlTestCase(unittest.TestCase):
    def setUp(self):
        os.system("cp coba coba~")
        self.file_path = os.path.join(THIS_DIR, "coba")

    def tearDown(self):
        os.system("rm coba")
        os.system("mv coba~ coba")

    def test_get_next_path(self):
        soup = make_soup(self.file_path)
        next_path = get_next_path(soup)
        self.assertEqual(next_path['href'], "coba")

    def test_replace_path(self):
        soup = make_soup(self.file_path)
        next_path = get_next_path(soup)
        replaced_path = replace_path(next_path, "hello")
        self.assertEqual(replaced_path, "hello")

    def test_replace(self):
        replace(self.file_path, os.path.join(THIS_DIR, "cobabaru"))
        soup = make_soup(self.file_path)
        next_path = get_next_path(soup)
        self.assertEqual(next_path['href'], os.path.join(THIS_DIR, "cobabaru"))

    def test_increase_file_name(self):
        file_name = increase_file_name(self.file_path)
        self.assertEqual(file_name, self.file_path + "2")

    def test_increase_file_name_2(self):
        file_name = increase_file_name(os.path.join(THIS_DIR, "rumah+sakit2"))
        self.assertEqual(file_name, os.path.join(THIS_DIR, "rumah+sakit3"))

if __name__ == "__main__":
    def get_abs_paths():
        import glob
        return [os.path.join(THIS_DIR, x) for x in glob.glob("rumah+sakit*")]

    for file_name in get_abs_paths():
        increased_file_name = increase_file_name(os.path.join(THIS_DIR,
                                                              file_name))
        replace(file_name, increased_file_name)

    print(get_abs_paths())

    unittest.main()
