# 1. import
import unittest

# 2. class - 만들고 상속
class TestStringUtils(unittest.TestCase):

    # 3. 각 테스트 함수 제작
    def test_upper(self):    
        """소문자를 대문자로 바꾸는 기능 확인"""
        result = "hello".upper()
        # 4. 검증
        self.assertEqual(result, "HELLO")

    def test_lower(self):
        """대문자를 소문자로 바꾸는 기능 확인"""
        result = "WORLD".lower()
        self.assertEqual(result, "world")

    def test_strip(self):
        """앞뒤 공백을 지우는 기능 확인"""
        result = "  hello  ".strip()
        self.assertEqual(result, "hello")

# 5. unittest.main() 
if __name__ == '__main__':
    unittest.main()