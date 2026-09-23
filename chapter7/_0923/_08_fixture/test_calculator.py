import pytest

class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ValueError("0으로 나눌 수 없습니다")
        return a / b


# fixture 없이
def test_add_without_fixture():
    calc = Calculator()
    result = calc.add(2,3)
    assert result == 5

def test_subtract_without_fixture():
    calc = Calculator()
    result = calc.subtract(10,3)
    assert result == 7


# fixture 설정 키워드
@pytest.fixture
def calculator():
    return Calculator()

def test_add_with_fixture(calculator):
    result = calculator.add(2,3)
    assert result == 5

def test_subtract_with_fixture(calculator):
    result = calculator.subtract(10,3)
    assert result == 7