import unittest
from string_processor import StringProcessor


class TestStringProcessor(unittest.TestCase):


    def setUp(self):
        self.sp = StringProcessor()

    # reverse
    # - 성공 4-5
    # - 1글자
    def test_reverse_normal(self):        
        result = self.sp.reverse("hello")
        self.assertEqual(result, "olleh")
        
    def test_reverse_one_char(self):
        result = self.sp.reverse("a")
        self.assertEqual(result, "a")

    # count_vowels
    # - 소문자
    # - 대문자
    def test_count_vowels_lowercase(self):
        result = self.sp.count_vowels("hello")
        self.assertEqual(result, 2)

    def test_count_vowels_uppercase(self):
        result = self.sp.count_vowels("AEIOU")
        self.assertEqual(result, 5)


    # count_vowels
    # 성공
    # 실패
    def test_is_palindrome_Pass(self):
        result = self.sp.is_palindrome("level")
        # self.assertEqual(result, True)
        self.assertTrue(result)

    def test_is_palindrome_Fail(self):
        result = self.sp.is_palindrome("hello")
        # self.assertEqual(result, False)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()