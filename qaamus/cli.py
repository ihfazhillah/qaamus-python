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
    parser.add_argument(
           "-p", "--pegon",
           action="store",
           metavar="NAMA",
           help="Mengartikan mem-pegon-kan query")
    parser.add_argument(
           "-P", "--pegon-instruction",
           action="store_true",
           help="Instruksi layanan terjemah pegon")
    return parser


def get_parser(parser):
    return parser.parse_args()


def main():
    namespace = get_parser(add_parser())
    if namespace.idar:
        print(api.idar(namespace.idar))

    elif namespace.angka:
        print(api.angka(namespace.angka))

    elif namespace.angka_instruction:
        print(api.angka_instruction())

    elif namespace.pegon:
        print(api.pegon(namespace.pegon))

    elif namespace.pegon_instruction:
        print(api.pegon_instruction())

if __name__ == "__main__":
    main()
