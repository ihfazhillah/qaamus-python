class QaamusRouter(object):
    def __init__(self):
        self.routers = {}

    def register(self, layanan, layanan_func):
        self.routers.update({layanan: layanan_func})

    def get_controller(self, layanan, *args, **kwargs):
        try:
            return self.routers[layanan](*args, **kwargs)
        except KeyError:
            return "Layanan tidak ditemukan."
