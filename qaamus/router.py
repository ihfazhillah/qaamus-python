class QaamusRouter(object):
    """Handle routering layanan in qaamus-python controller."""
    def __init__(self):
        self.routers = {}

    def register(self, layanan, layanan_func):
        """Registering router."""
        self.routers.update({layanan: layanan_func})

    def get_controller(self, layanan, *args, **kwargs):
        """call the function tergantung dengan layanan."""
        try:
            return self.routers[layanan](*args, **kwargs)
        except KeyError:
            return "Layanan tidak ditemukan."
