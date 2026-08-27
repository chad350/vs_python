# for [1,2,3,4,5,6]


# while
# 무한 루프

# loop     1    2    3    4     5      ... 11
# total  : 1    3    6    10    15    
# i      : 2    3    4    5     6          10

total = 0
i = 1

while i <= 10 : 
    total += i
    i += 1

print("1 - 10 의 합계 :", total)


print("직업을 선택해 주세요.")
print("1. 전사   2. 도적    3. 궁수    4. 마법사")

while True :
    select_input = input()
    select = int(select_input)

    if select >= 1 and select <= 4 :
        break

    print("입력을 확인해주세요.")
  
print("직업선택을 완료했습니다.")


# set
numbers = [ 1, 2, 52, 20, 99, 50, 60, 60, 52, 60]

# 앞에 있는거 하나만 지우게
numbers.remove(60)

# [ 1, 2, 52, 20, 99, 50, 52, 60]
while True :

    if 60 in numbers:
        numbers.remove(60)

    else : 
        break

while 60 in numbers :
    numbers.remove(60)