from qaamus import Qaamus


def idar(query, pretty=False):
    return Qaamus().terjemah("idar", query, pretty)


def angka(query, pretty=False):
    return Qaamus().terjemah("angka", query, pretty)


def angka_instruction(pretty=False):
    return Qaamus().terjemah("angka_instruction", pretty)
