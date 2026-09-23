import unittest

class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, name, price):
        self.items.append({"name": name, "price": price})

    def get_total(self):
        total = 0
        for item in self.items:
            total = total + item["price"]
        return total

    def clear(self):
        self.items = []


class TestShoppingCart(unittest.TestCase):

    def setUp(self):
        print("\n🛒 setUp: 새 장바구니 생성")
        self.cart = ShoppingCart()

    def test_add_item(self):
        """상품 추가 테스트"""
        print("   테스트: 상품 추가")
        self.cart.add_item("포션", 100)
        self.assertEqual(len(self.cart.items), 1)

    def test_clear_cart(self):
        """장바구니 비우기 테스트"""
        print("   테스트: 장바구니 비우기")
        self.cart.add_item("포션", 100)
        self.cart.clear()
        self.assertEqual(len(self.cart.items), 0)

    def test_get_total(self):
        """총액 계산 테스트"""
        print("   테스트: 총액 계산")
        self.cart.add_item("포션", 100)
        self.cart.add_item("검", 500)
        self.assertEqual(self.cart.get_total(), 600)

    def test_initial_items(self):
        """초기 상품 개수 확인"""
        print("   테스트: 초기 상품 개수")
        self.assertEqual(len(self.cart.items), 0)


if __name__ == '__main__':
    unittest.main()