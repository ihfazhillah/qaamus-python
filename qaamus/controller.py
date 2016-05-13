import view
import parsers


def idar_controller(soup_object, make_soup):
    data = parsers.IndAraParser(soup_object).get_idar(make_soup)
    rendered = view.View().render(data)
    return rendered

def angka_controller(soup_object):
    data = parsers.AngkaParser(soup_object).get_arti_master()
    rendered = view.View().render(data)
    return rendered

def pegon_controller(soup_object):
    data = parsers.PegonParser(soup_object).get_arti_master()
    rendered = view.View().render(data)
    return rendered

def angka_instruksi_controller(soup_object):
    data = parsers.AngkaParser(soup_object).get_instruction()
    rendered = view.View().render(data, layanan="Angka")
    return rendered

def pegon_instruksi_controller(soup_object):
    data = parsers.PegonParser(soup_object).get_instruction()
    rendered = view.View().render(data, layanan="Pegon")
    return rendered

