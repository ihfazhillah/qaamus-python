import unittest
from router import QaamusRouter


def coba():
    return "aku"


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


if __name__ == "__main__":
    unittest.main()
