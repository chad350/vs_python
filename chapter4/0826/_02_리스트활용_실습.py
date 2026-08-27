numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# 실습1. 2자리 - 6자리 숫자만 출력
# 슬라이스
print(numbers[1:6])

# 실습2. 4 를 삭제하고 출력
numbers.remove(4)
print(numbers)

# 실습3. 25 를 추가하고 출력
numbers.append(25)
print(numbers)

# 실습4. 100 4번때에 추가고 출력
numbers.insert( 3 , 100)
print(numbers)