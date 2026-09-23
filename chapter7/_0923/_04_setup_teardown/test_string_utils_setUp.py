# 1. import
import unittest

# 2. class - 만들고 상속
class TestStringUtils(unittest.TestCase):
    done_test_case = []

    def setUp(self):
        print("case 초기화")
        self.done_test_case = []

    # 3. 각 테스트 함수 제작
    def test_upper(self):    
        """소문자를 대문자로 바꾸는 기능 확인"""

        self.done_test_case.append("test_upper")
        print(self.done_test_case)

        result = "hello".upper()
        # 4. 검증
        self.assertEqual(result, "HELLO")

    def test_lower(self):
        """대문자를 소문자로 바꾸는 기능 확인"""

        self.done_test_case.append("test_lower")
        print(self.done_test_case)
        
        result = "WORLD".lower()
        self.assertEqual(result, "world")

    def test_strip(self):
        """앞뒤 공백을 지우는 기능 확인"""

        self.done_test_case.append("test_strip")
        print(self.done_test_case)

        result = "  hello  ".strip()
        self.assertEqual(result, "hello")

# 5. unittest.main() 
if __name__ == '__main__':
    unittest.main()