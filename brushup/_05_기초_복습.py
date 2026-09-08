test = [1,2,3,4]

for x in test:
    pass

for x in range(0,10):
    pass


# 반복문(리스트) + 조건문
# 실습1. range 로 1부터 5까지 돌면서 출력 -> 1번째 반복 시작 ... 5번째 반복 시작
for i in range(1 , 6):
    print(i,"번째 반복 시작")


potions = ["빨간 포션", "파란 포션", "빨간 포션", "노란 포션", "빨간 포션"]
damages = [12, 30, 25, 8, 40]

# 실습2. potions 를 for 문으로 하나씩 출력
for p in potions:
    print(p)

# 실습3. damages 를 for 문으로 돌면서 20 이상인 값만 출력 -> 30, 25, 40
for d in damages:
    if d >= 20 :
        print(d)

# 실습4. damages 의 합계를 출력 
print("damage 의 합계 :",sum(damages))

total = 0
for d in damages:
    total+=d
print("damage 의 합계 :",total)


# 실습5. potions 에 "빨간 포션"이 몇 개인지 출력
red_count = potions.count("빨간 포션")
red_count = 0
for p in potions:
    if p == "빨간 포션":
        red_count += 1

# 문자열
user_id = "Knight_302"
result = "PASS"
log = "login|PASS|0.8"

# 실습6. user_id 의 글자 수 출력 - len()
print(len(user_id))

# 실습7. user_id 를 전부 소문자로 바꿔서 출력 - lower() 
print(user_id.lower())

# 실습8. user_id 가 "Knight"로 시작하는지 확인 - startswith()
print(user_id.startswith("Knight"))

# 실습9. result 가 "PASS"이면 통과, 아니면 실패 를 출력 - if
if result == "PASS":
    print("통과")
else:
    print("실패")

# 실습10. log 를 "|" 기준으로 나눠서 두 번째 인덱스를 출력 -> PASS -> split()
strs = log.split("|")
# 0 1 2
print(strs[1]) # PASS


# 클래스 (상속 X)
# 실습11. 클래스 Potion 만들기 [ name, heal 이라는 속성을 저장할 수 있도록 ]
# 실습12. red_potion 이라는 인스턴스 생성 ("빨간 포션", 50) -> name 출력
# 실습13. blue_potion 이라는 인스턴스 생성 ("파란 포션", 100) -> heal 출력
# 실습14. Potion 에 info() 메서드 추가 -> 빨간 포션 회복량 50

class Potion :
    def __init__(self, name, heal):
        self.name = name
        self.heal = heal

    def info(self):
        print(self.name, self.heal)

red_potion = Potion("빨간물약", 50)
print(red_potion.name)

blue_potion = Potion("파란물약", 100)
print(blue_potion.heal)