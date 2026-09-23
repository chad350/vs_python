from calculator import add, subtract

def test_add_positive():
    """양수 덧셈 테스트"""
    result = add(2, 3)
    assert result == 5

def test_add_negative():
    """음수 덧셈 테스트"""
    result = add(-1, 1)
    assert result == 0

def test_subtract():
    """덧셈 테스트"""
    result = subtract(10, 3)
    assert result == 5