from .qaamus import Qaamus


def idar(query):
    return Qaamus().terjemah("idar", query)


def angka(query):
    return Qaamus().terjemah("angka", query)


def angka_instruksi():
    return Qaamus().terjemah("angka_instruksi")


def pegon(query):
    return Qaamus().terjemah("pegon", query)


def pegon_instruksi():
    return Qaamus().terjemah("pegon_instruksi")
