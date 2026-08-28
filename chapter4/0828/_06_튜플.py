var1 = "문자입니다."
num = 11

# 리스트
# 데이터를 추가 / 제거 할 수 있음
characters = ["안녕", "hi"]
numbers = [5, 7, 8, 9 , 10]



# 튜플
# 데이터를 추가 / 제거 - X
# 한번 만들어진 데이터를 고정
# 가능 - 인덱스, 슬라이스, len, in, count, index, for
# 불가능 - apeed remove sort
player = ( "chad", 20, "전사"  )
monster = "오크", 15, "전사"


item = ( "낡은 단검", 120, "일반" )

# 언패킹
name, price, grade = item  # 가능

name, price , _ = item  # 사용하지 않는 것은 _ 로 표현
name, _ , grade = item  # 사용하지 않는 것은 _ 로 표현