import unittest
from router import QaamusRouter


def coba():
    return "aku"


def coba_arg(arg):
    return arg


class QaamusRouterTestCase(unittest.TestCase):
    def test_initial_testing(self):
        router = QaamusRouter()
        self.assertEqual(router.routers, dict())

    def test_add_new_router(self):
        router = QaamusRouter()
        router.register("coba", coba)
        self.assertEqual(router.routers['coba'](), "aku")

    def test_get_router(self):
        router = QaamusRouter()
        router.register("coba", coba)
        result = router.get_controller("coba")
        self.assertEqual(result, "aku")

    def test_get_router_with_wrong_key(self):
        router = QaamusRouter()
        router.register("coba", coba)
        result = router.get_controller("bb", "a")
        self.assertEqual(result, "Layanan tidak ditemukan.")

    def test_get_router_with_arg(self):
        router = QaamusRouter()
        router.register("coba_arg", coba_arg)
        result = router.get_controller("coba_arg", "aku")
        self.assertEqual(result, "aku")


if __name__ == "__main__":
    unittest.main()
