# 기획 - 게임사에서 미리 데이터
# 직업별 능력치
job_list = [ "전사", "도적", "마법사" ]
# hp
hp_list = [ 100, 80 , 70 ]
# mp
mp_list = [ 20, 30 , 50 ]
# 공격력
atk_list = [ 15, 20, 10 ]
# 방어력
defence_list = [ 30, 10, 5 ]

# 유저 데이터
nickname = ""
job = ""
level = 1
hp = 0
mp = 0
atk = 0
defence = 0
gold = 1500


# 캐릭터 생성
print ("이름을 입력해주세요.")
nickname = input()

print ("직업을 선택해 주세요.")
print ("1. 전사    2. 도적     3. 마법사") 
input_number = input()
number = int(input_number) - 1

job = job_list [ number] 
hp = hp_list [ number ] 
mp = mp_list [ number] 
atk = atk_list [ number] 
defence = defence_list [ number ] 


print("\033[2J\033[H")

print("[캐릭터 정보]")
print("닉네임 :",nickname)
print("직업",job)
print("Lv.",level)
print("hp :",hp)
print("mp :",mp)
print("공격력 :",atk)
print("방어력 :",defence)


input("상점을 가고 싶으면 enter 를 눌러주세요.")
print("\033[2J\033[H")

item_list = [ "hp 물약", "mp 물약", "지도"]
cost_list = [ 800, 1500, 2000 ]

print ("구매하고 싶은 아이템을 입력해주세요.")
print ("1. hp 물약    2. mp 물약     3. 지도") 
input_item = input()
item_number = int(input_item) - 1

item_cost = cost_list[item_number]
item_name = item_list[item_number]

can_buy = gold >= item_cost

gold -= item_cost

if can_buy : 
    print(item_name, "을 구매했습니다. 잔돈:",gold)
else :
    print(item_name, "을 구매하지 못했습니다.")