from qaamus import Qaamus


def idar(query, pretty=False):
    return Qaamus().terjemah("idar", query, pretty)


def angka(query, pretty=False):
    return Qaamus().terjemah("angka", query, pretty)


def angka_instruction(pretty=False):
    return Qaamus().terjemah("angka_instruction", pretty)


def pegon(query, pretty=False):
    return Qaamus().terjemah("pegon", query, pretty)


def pegon_instruction(pretty=False):
    return Qaamus().terjemah("pegon_instruction", "surabaya", pretty)
