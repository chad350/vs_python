# 1. 리스트 (5)
print("1. 리스트 (5문항)")

items = ["낡은 단검", "가죽 갑옷", "포션", "포션", "마나 물약", "포션"]
prices = [1200, 3500, 300, 300, 450, 300]

# 실습1. items 에 아이템이 몇 개 들어 있는지 출력
print(len(items))

# 실습2. 첫 번째 아이템과 마지막 아이템을 출력 [인덱스 사용] -> 낡은 단검, 포션
print(items[0])
print(items[-1])

# 실습3. items 에 "포션"이 몇 개인지 출력
print(items.count("포션"))

# 실습4. items 맨 끝에 "낡은 방패"를 추가하고, "마나 물약"을 제거한 뒤 전체 출력
items.append("낡은 방패")
items.remove("마나 물약")
print(items)

# 실습5. prices 를 비싼 순서로 정렬해서 출력 [원본이 변하면 안됨]
print(sorted(prices, reverse=True))


# 2. 반복문 (5)
print("\n\n2. 반복문 (5문항)")
monsters = ["슬라임", "고블린", "오크", "리자드맨", "골렘"]
levels = [1, 3, 5, 7, 10]

# 실습6. monsters 를 for 문으로 하나씩 출력
for monster in monsters :
    print(monster)

# 실습7. 1부터 10까지 출력 [range 사용]
for number in range(1, 11) :
    print(number)


# 실습8. levels 의 합계를 누적으로 구해서 출력 [sum() 금지] -> 26    [생각이 안난다면 마지막에]
total = 0
for level in levels : 
    total += level
print(total)


# 실습9. monsters 와 levels 를 짝지어 출력 [zip 사용] -> [ 이름 : 슬라임 , Level : 1 ]
for monster, level in zip(monsters, levels) :
    print("[ 이름 :",monster,", Level :",level," ]")

# 실습10. while 문으로 5부터 1까지 거꾸로 출력
# num  = 5 -> 4 -> 3 -> 2 -> 1 
num = 5
while num >= 1: 
    print(num)
    num -= 1

# 3. 문자열 (4)
print("\n\n3. 문자열 (5문항)")

code = "WPN-0450-R"
log = "  STAGE-03|CLEAR|1200  "
names = ["기사", "마법사", "궁수"]

# 실습11. code 를 "-" 기준으로 나눠서 리스트로 출력
print(code.split("-"))

# 실습12. log 양쪽 끝의 공백을 제거해서 출력
print(log.strip())

# 실습13. log 의 "CLEAR"를 "FAIL"로 바꿔서 출력
print(log.strip().replace("CLEAR","FAIL"))

# 실습14. names 를 ", "로 이어 붙여서 출력 -> 기사, 마법사, 궁수
print(", ".join(names))




# 응용 실습 - 상점 계산기
print("\n\n응용 실습 - 상점 계산기")
items = ["낡은 단검", "가죽 갑옷", "포션", "마나 물약", "화살 묶음"]
prices = [1200, 3500, 300, 450, 200]
gold = 900
cart = []
total = 0


for item, price in zip(items, prices) :     

    if price <= 500 :
        cart.append(item)
        total += price

print("구매목록 :",cart)
print("합계 :",total)


if total <= gold:
    result = gold - total
    print("구매 가능 / 잔액:", result)
else :
    result = total - gold
    print("골드 부족 / 부족분:", result)


# 1) 가격이 500 골드 이하인 아이템만 구매 목록 cart 에 담기 [for + append]
# 2) cart 에 담은 아이템들과 가격 합계 구하기

# 구매 목록: ['포션', '마나 물약', '화살 묶음']
# 합계: 950

# 3) 소지 골드와 비교해서 판정 출력
#    -> 살 수 있으면: 구매 가능 / 잔액: OO
#    -> 부족하면:     골드 부족 / 부족분: OO
