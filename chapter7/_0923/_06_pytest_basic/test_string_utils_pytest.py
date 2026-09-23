from string_utils import reverse_string

def test_reverse_string_nomarl():
    """일반 문자열"""

    # Arrange - 데이터 준비 
    check_data = "hello"
    expect_data = "olleh"

    # Act - 테스트랑 기능 실행 : reverse_string
    result = reverse_string(check_data)

    # Assert - 실행 결과 검증
    assert result == expect_data
    # assert reverse_string("hello") == "olleh"

def test_reverse_string_empty():
    """빈 문자열"""
    result = reverse_string("")
    assert result == ""

def test_reverse_string_one_char():
    """한 글자"""
    result = reverse_string("a")
    assert result == "a"

def test_reverse_string_palindrome():
    """회문"""
    result = reverse_string("level")
    assert result == "level"

def test_reverse_string_with_space():
    """공백 포함"""
    result = reverse_string("hello world")
    assert result == "dlrow olleh"