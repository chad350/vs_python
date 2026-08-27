# 실습1. 0부터 4까지  출력
for i in range(5):
    print(i)

# 실습2. 1부터 5까지  출력
for i in range(1, 6):
    print(i)

for i in range(5):
    print(i+1)

# 실습3. 0부터 10까지 2씩 건너뛰며 출력
for i in range(0, 11, 2):
    print(i)


bag = ["낡은 단검", "가죽 갑옷", "이끼 반지"]

# 실습4. 1번부터 번호를 붙여 출력
for i, item in enumerate(bag, start=1) : 
    print(i, item)


names = ["이끼 슬라임", "동굴 박쥐", "돌 골렘"]
hps   = [30, 60, 150]

# 실습5. 이름과 체력을 나란히 출력
for name, hp in zip(names, hps):
    print(name, hp)


items = ["포션", "낡은 검", "철 갑옷", "귀환 스크롤", "지팡이"]
prices = [120, 450, 1200, 200, 600]

# 실습6. 500골드로 살 수 있는 것만 표시 
# [아이템 이름  가격]
# 예 [포션 120G]

for item, price in zip(items, prices):
    if price <= 500 :
        print("[",item, price, "G]")