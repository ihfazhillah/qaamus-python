import argparse
import api


def add_parser():
    parser = argparse.ArgumentParser(description="Terjemah Indonesia Arab")
    parser.add_argument(
            "query",
            metavar="Query",
            help="Sebuah query yang ingin dicari artinya")
    parser.add_argument(
            "-i", "--idar",
            action="store_true",
            help="Mengartikan ke Bahasa Arab dari suatu query")
    parser.add_argument(
            "-a", "--angka",
            action="store_true",
            help="Mengartikan query berupa angka kedalam bahasa arab")
    return parser


def get_parser(parser):
    return parser.parse_args()


def main():
    namespace = get_parser(add_parser())
    if namespace.idar:
        print(api.idar(namespace.query, pretty=True))
    elif namespace.angka:
        print(api.angka(namespace.query, pretty=True))

if __name__ == "__main__":
    main()
