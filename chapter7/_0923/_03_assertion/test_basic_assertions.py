import unittest


class TestBasicAssertions(unittest.TestCase):

    def test_assertEqual_with_numbers(self):
        """숫자 비교: assertEqual"""
        damage = 50 - 20
        self.assertEqual(damage, 30)

    def test_assertEqual_with_strings(self):
        """문자열 비교: assertEqual"""
        name = "Knight".upper()
        self.assertEqual(name, "KNIGHT")

    def test_assertIsNone(self):
        """None 검증: assertIsNone"""
        inventory = {"sword": 1}
        result = inventory.get("shield")
        self.assertIsNone(result)

    def test_assertIs_same_object(self):
        """동일 객체 검증: assertIs"""
        bag = ["potion"]
        same_bag = bag
        self.assertIs(bag, same_bag)

    def test_assertTrue_and_assertFalse(self):
        """불리언 검증: assertTrue, assertFalse"""
        hp = 10
        self.assertTrue(hp > 0)
        self.assertFalse(hp > 100)


if __name__ == '__main__':
    unittest.main()
