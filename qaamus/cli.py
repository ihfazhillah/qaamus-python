import sys
import argparse
from .__init__ import __version__
from . import api


version = "Versi Qaamus-python: {}".format(__version__)


class QaamusArgParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        super(QaamusArgParser, self).__init__(*args, **kwargs)
        self.add_argument("-v", "--version",
                          action="store_true",
                          help="Print version program dan exit")
        self.args = {}

    def process(self):
        self.args = vars(self.parse_args())
        if self.args['version']:
            print(version)
            sys.exit(0)


class IDARArgParser(QaamusArgParser):
    def __init__(self, *args, **kwargs):
        super(IDARArgParser, self).__init__(*args, **kwargs)
        self.description = "Terjemahkan query indonesia ke arab"
        self.add_argument("QUERY",
                          help="Query yang akan diterjemahkan")

    def process(self):
        super(IDARArgParser, self).process()
        if self.args['QUERY']:
            print(api.idar(self.args['QUERY']))
        else:
            return False
        return True


class AngkaArgParser(QaamusArgParser):
    def __init__(self, *args, **kwargs):
        super(AngkaArgParser, self).__init__(*args, **kwargs)
        self.description = "Terjemahkan angka ke arab"

        self.add_argument("QUERY",
                          nargs="?",
                          help="Query yang akan diterjemahkan")
        self.add_argument("-i", "--instruksi",
                          action="store_true",
                          help="Print instruksi terjemah angka")

    def process(self):
        super(AngkaArgParser, self).process()
        if self.args['QUERY']:
            print(api.angka(self.args['QUERY']))
        elif self.args['instruksi']:
            print(api.angka_instruksi())
        else:
            return False
        return True


class PegonArgParser(QaamusArgParser):
    def __init__(self, *args, **kwargs):
        super(PegonArgParser, self).__init__(*args, **kwargs)
        self.description = "Terjemah pegon"

        self.add_argument("QUERY",
                          nargs="?",
                          help="Query yang akan diterjemahkan")
        self.add_argument("-i", "--instruksi",
                          action="store_true",
                          help="Print instruksi terjemah pegon")

    def process(self):
        super(PegonArgParser, self).process()
        if self.args['QUERY']:
            print(api.pegon(self.args['QUERY']))
        elif self.args['instruksi']:
            print(api.pegon_instruksi())
        else:
            return False
        return True


def main():
    args = sys.argv
    if len(args) > 1:
        del args[0]

    mode_dict = {'idar': IDARArgParser,
                 'angka': AngkaArgParser,
                 'pegon': PegonArgParser,
                 'version': None}

    if len(args) == 0 or args[0] not in mode_dict:
        print("Perintah yang tersedia:\n")
        print("=======================\n")
        print(", ".join(mode_dict.keys()))
        sys.exit(1)

    mode = args[0]
    if mode == 'version':
        print(version)
        sys.exit(0)
    else:

        parser = mode_dict[mode]()
        if not parser.process():
            parser.print_help()
