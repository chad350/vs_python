prices_1 = [450, 120, 1200, 200, 800]

# 실습1. 오름차순 출력 [원본이 변하면 안됨]
print(sorted(prices_1))
# 실습2. 원본 출력
print(prices_1)

# 실습3. 오름차순 출력 [원본이 변해도 됨]
prices_1.sort()
print(prices_1)

# 실습4. 내림차순 출력 [원본이 변해도 됨]
prices_1.sort(reverse=True)
print(prices_1)


prices_2 = [450, 120, 1200, 200, 800]

# 실습5. 비싼 순으로 3개만 출력
tmp_1 = sorted(prices_2, reverse=True) # [120, 200, 450, 800, 1200]
print(tmp_1[:3])

# 실습6. 싼 순으로 2개만 출력
tmp_2 = sorted(prices_2) # [120, 200, 450, 800, 1200]
print(tmp_2[:2])
