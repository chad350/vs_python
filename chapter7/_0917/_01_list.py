nums = [3, 8, 5, 12]

result_1 = []
for n in nums:
    if n >= 8:
        result_1.append(n)

# 리스트 컴프리헨션
result_2 = [ n for n in nums if n >= 8 ]
print(result_2)

result_3 = [ n + 1 for n in nums if n >= 8 ]
print(result_3)

result_4 = [ n * 2 for n in nums if n >= 8 ]
print(result_4)


# 원본 그대로 - 복사
[n for n in nums] 

# 조건에 맞춰 필터링     조건     
[n for n in nums  if n >= 8 ] 

# 값만 바꿔서 저정    필터링 X     
[ n * 2   for n in nums] 

# 값도 바꾸고                필터링 까지해서 저장
[ n * 2   for n in nums   if n >= 8] 


print("연습")

# 5보다 큰 수만 저장 (초과)
nums = [3, 8, 5, 12, 1, 7]
result_1 = [n for n in nums if n > 5]
print(result_1)

# 짝수만 저장  
nums = [3, 8, 5, 12, 1, 7]
result_2 = [n for n in nums if n % 2 == 0]
print(result_2)


# 2배로 바꿔서 저장
nums = [3, 8, 5, 12, 1, 7]
result_3 = [n * 2 for n in nums]
print(result_3)