import pytest

#                            문자열                       배열
#                          변수의 이름                   테스트케이스
#                         원하는 갯수만큼                                     
@pytest.mark.parametrize( "num, expected"  ,   [( 2 , 4 ),  # 1번째
                                                ( 3 , 6 ),  # 2번째
                                                ( 4 , 8 ),  # 3번째
                                                ( 5 , 10)] )# 4번째
def test_double(num, expected):

    print(f"\nnum : {num}    /    expected : {expected}")
    assert num * 2 == expected