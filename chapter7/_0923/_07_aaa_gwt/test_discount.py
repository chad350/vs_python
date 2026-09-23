def get_discount_price(price, discount_percent):
    """할인된 가격을 계산합니다"""
    discount = price * discount_percent / 100
    return price - discount


def test_discount_aaa():
    # Arrange (준비)
    price = 10000
    discount_percent = 20
    expected = 8000

    # Act (실행)
    result = get_discount_price(price, discount_percent)

    # Assert (검증)
    assert result == expected


def test_discount_gwt():
    # Given (준비)
    price = 5000
    discount_percent = 10
    expected = 4500

    # When (실행)
    result = get_discount_price(price, discount_percent)

    # Then (검증)
    assert result == expected