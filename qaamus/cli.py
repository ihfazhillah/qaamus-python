import argparse
import api


def add_parser():
    parser = argparse.ArgumentParser(description="Terjemah Indonesia Arab")
    parser.add_argument(
            "-i", "--idar",
            action="store",
            metavar="INDONESIA",
            help="Mengartikan ke Bahasa Arab dari suatu query")
    parser.add_argument(
            "-a", "--angka",
            action="store",
            metavar="ANGKA",
            help="Mengartikan query berupa angka kedalam bahasa arab")
    parser.add_argument(
           "-A", "--angka-instruction",
           action="store_true",
           help="Instruksi layanan terjemah angka")
    return parser


def get_parser(parser):
    return parser.parse_args()


def main():
    namespace = get_parser(add_parser())
    if namespace.idar:
        print(api.idar(namespace.idar, pretty=True))

    elif namespace.angka:
        print(api.angka(namespace.angka, pretty=True))

    elif namespace.angka_instruction:
        print(api.angka_instruction(pretty=True))

if __name__ == "__main__":
    main()
