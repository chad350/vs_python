item = "낡은 단검"
price = 500

print("[ 이름 :",item, " , 가격 :",price,"G ]")

# 스트링 포맷
print("[ 이름 : {} , 가격 : {} G ]".format( item ,  price ))



# {}
print(f"중괄호 자체가 문자열에 포함되었으면 하는 경우 : {{}} ")

# ' 따옴표,   " 쌍따옴표
# 방법 1
print("안녕하세요 제 이름은 '염예찬' 입니다.")
print('안녕하세요 제 이름은 "염예찬" 입니다.')

# 방법 2
print("안녕하세요 제 이름은 \"염예찬\" 입니다.  '인천'에서 왔어요 ")

# 방법 3
print("""안녕하세요 제 이름은 "염예찬" 입니다.
'인천'에서 왔어요""")






# f 스트링
# 하나의 문자열에 변수를 섞어서 구성
# 맨 앞에 f 키워드 추가
# { } <- 구분
print(f"[ 이름 : {item}  , 가격 : {price} G ]")

# 소수점 조절
pi = 3.14159
print(f"pi : {pi}")
print(f"pi : {pi:.0f}")
print(f"pi : {pi:.1f}")
print(f"pi : {pi:.2f}")

# 1000의 자리 숫자 표시
num = 1234567
print(f"num : {num:,}")

print(f"num : {num:.2f}")
print(f"num : {num:,.2f}")

# 백분율 표시
rate = 0.4567
print(f"rate : {rate:.1%}")
print(f"rate : {rate:.2%}")
print(f"rate : {rate:.3%}")

# 패딩 붙이기
num = 42
print(f"num : {num}")       # 42
print(f"num : {num:03d}")   # 042
print(f"num : {num:04d}")   # 0042
print(f"num : {num:4d}")    #   42

# 문자 정렬
name = "Chad"
print(f"name : {name}")
print(f"name : {name:<10}")  # 왼쪽 정렬
print(f"name : {name:>10}")  # 오른쪽 정렬
print(f"name : {name:^10}")  # 가운데 정렬
print(f"name : {name:#<10}")  # 채우기 문자 : #
print(f"name : {name:.>10}")  # 채우기 문자 : .
print(f"name : {name:*^10}")  # 채우기 문자 : *


name  = "이끼 슬라임"
hp    = 47
price = 1234567
rate  = 0.4567
pi    = 3.14159

# 실습1. "이끼 슬라임의 체력은 47입니다" 출력
print(f"{name}의 체력은 {hp}입니다")

# 실습2. pi 를 소수 둘째 자리까지
print(f"pi : {pi:.2f}")

# 실습3. price 에 천 단위 쉼표 붙이기
print(f"price : {price:,}")

# 실습4. price 를 쉼표 + 소수 둘째 자리까지
print(f"price : {price:,.2f}")

# 실습5. rate 를 백분율로 [소수 첫째 자리까지]
print(f"rate : {rate:.1%}")

# 실습6. hp 를 세 자리 0 채움으로 (047)
print(f"hp : {hp:03d}")

# 실습7. name 을 왼쪽 정렬 12칸으로 출력하고 뒤에 | 붙이기
print(f"name : {name:<12}|")

# 실습8. name 을 오른쪽 정렬 12칸으로
print(f"name : {name:>12}|")

# 실습9. name 을 가운데 정렬 12칸, 채움문자 *
print(f"name : {name:*^12}|")