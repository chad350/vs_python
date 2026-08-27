number = [2, 5, 29, 20, 80, 90, 52, 80]
words = ['banana', 'Apple', 'cherry', 'Date']

# len - 배녕의 갯수를 확인
# count - 해당 요소가 몇개 있는 체크
# print(number.count(80))

# 정렬 1
# number.sort()
# number.sort(reverse = True)  정렬 순서 옵션을 추가 지정 가능
# words.sort( key=str.lower)   문자도 정렬이 가능하고 옵션을 추가 지정 가능
# 영어랑 한글이 있다면 영어우선

# 정렬 2
# tmp = sorted(number)

# print("sum :", sum(number))
# print("min :", min(number))
# print("max :", max(number))

# in - 배열안에서 데이터 찾는데 있는지 없는지 확인 -> bool
# print("Apple" in words)
# print("Orange" in words)

# index - 배열안에서 데이터를 찾는데 어디(index)있는지 알려주는 것 -> int
# 없는 대상을 가리키면 오류를 발생시킵니다.
# print(words.index("Apple"))
# print(words.index("Orange"))


# 절대값 - abs()
# n_num = -3.6
# print(abs(n_num))


# 반올림 - round()
# print(round(1.2)) # 1
# print(round(1.7)) # 2
# print(round(1.5)) # 2  -  올림처리
# print(round(3.14159, 2)) # 3.14 - 자리수 지정
