from .controller import router
from .utils import soupping, build_url


class Qaamus:

    def terjemah(self, layanan, query=""):
        """
        Return terjemahan tergantung dengan **layanan** apa yang dia pilih,
        dan **query** apa yang dia pakai.
        Adapun *layanan* di [Qaamus](qaamus.com) saat ini terdapat 3 layanan:
            * Indonesia Arab
            * Angka
            * Terjemah nama
        Adapun *layanan* yang ada di qaamus-python ini adalah:
            * idar
            * angka
            * pegon
            * angka_instruksi
            * pegon_instruksi
        Sedangkan *query* adalah query pencarian anda"""
        if layanan in ['idar', 'angka', 'pegon']:
            url_layanan = layanan
        elif layanan in ['angka_instruksi', 'pegon_instruksi']:
            url_layanan = layanan.split("_")[0]
            query = "123"

        url = build_url(query, layanan=url_layanan)
        soup = soupping(url)
        return router.get_controller(layanan, soup, soupping)
