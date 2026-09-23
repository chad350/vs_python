import unittest # standard libaray -> 설치도 안해도 되는 기본 기능
from calculator import add

# uniittest <- 요 모듈은 클래스 단위 - 테스트 케이스 만들어서 실행
# 상속 - 이미 unittest 만들어둔 TestCase 의 기능을 활용한 클래스를 제작 
class TestCalculator(unittest.TestCase):

    # 메서드 단위로 실행한 테스트를 만듭니다.
    def test_add_positive_numbers(self):
        """양수의 덧셈을 테스트"""
        result = add(2, 3)
        self.assertEqual(result, 5) # 2개의 값이 맞는지 확인하는 기능
        # 2 + 3 = 5 인지 확인하는 기능

    def test_add_negative_numbers(self):
        """음수의 덧셈을 테스트"""
        result = add(-1, -1)
        self.assertEqual(result, -2)
        # -1 + -1 = -2 인지 확인하는 기능


if __name__ == '__main__':
    unittest.main()



# 셀레니움
# find_element