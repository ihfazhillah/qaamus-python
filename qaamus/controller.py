from .router import QaamusRouter
from . import parsers, view


router = QaamusRouter()


def idar_controller(soup_object, make_soup, *args, **kwargs):
    data = parsers.IndAraParser(soup_object).get_idar(make_soup)
    rendered = view.View().render(data)
    return rendered
router.register("idar", idar_controller)


def angka_controller(soup_object, *args, **kwargs):
    data = parsers.AngkaParser(soup_object).get_arti_master()
    rendered = view.View().render(data)
    return rendered
router.register("angka", angka_controller)


def pegon_controller(soup_object, *args, **kwargs):
    data = parsers.PegonParser(soup_object).get_arti_master()
    rendered = view.View().render(data)
    return rendered
router.register("pegon", pegon_controller)


def angka_instruksi_controller(soup_object, *args, **kwargs):
    data = parsers.AngkaParser(soup_object).get_instruction()
    rendered = view.View().render(data, layanan="Angka")
    return rendered
router.register("angka_instruksi", angka_instruksi_controller)


def pegon_instruksi_controller(soup_object, *args, **kwargs):
    data = parsers.PegonParser(soup_object).get_instruction()
    rendered = view.View().render(data, layanan="Pegon")
    return rendered
router.register("pegon_instruksi", pegon_instruksi_controller)
