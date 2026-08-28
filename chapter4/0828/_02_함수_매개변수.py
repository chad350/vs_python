#        파라미터 / 매개변수
def error_msg( var ) :    
    print("\033[35mError", var, "\033[0m")


# Error 버그가 감지되었습니다.
# Error 서버가 공격받았습니다.


#           아규먼트 / 인자값
error_msg( "버그가 감지되었습니다." ) 
error_msg( "서버가 공격받았습니다." ) 


#             5
def double ( num ) :
    print( num * 2 )

#          30     10
def add ( num_1, num_2 ) :
    print( num_1 + num_2 )


# 1. 함수 - 더블
# 숫자를 2배로 부풀려서 출력
double( 5 )

# 2. 함수 - 더하기
# 숫자를 2개 전달하면 합쳐서 출력
add(10, 20)
add(30, 10)