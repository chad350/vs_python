item_name = ["철검", "연습용 검", "연습용 방패", "나무 지팡이"        ]
item_cost = [100,       150,          130,          200      ]
item_atk  = [15,          5,            0,           20      ]
item_def  = [0,           0,            5,           0       ]

gold = 140

inventory_name = [ ]
inventory_cost = [ ]
inventory_atk = [ ]
inventory_def = [ ]

# [상점]
# 0 - 철검  |  atk : 15    def : 0       100 G    [구매가능]
# 1 - 연습용 검 |  atk : 5  def : 0       150 G    [구매불가]
# 2 - 연습용 방패 |  atk : 0   def : 5     130 G    [구매가능]
# 4 - 나무 지팡이  |  atk : 20  def : 0    200 G    [구매불가]

# [인벤토리]
# 0 - 철검  |  atk : 15    def : 0




# print("0 - ", item_name[0], "|   atk :",item_atk[0], "   def :",item_def[0], " ", item_cost[0],"G")
# print("1 - ", item_name[1], "|   atk :",item_atk[1], "   def :",item_def[1], " ", item_cost[1],"G")
# print("2 - ", item_name[2], "|   atk :",item_atk[2], "   def :",item_def[2], " ", item_cost[2],"G")
# print("3 - ", item_name[3], "|   atk :",item_atk[3], "   def :",item_def[3], " ", item_cost[3],"G")


print("[상점]")
length = len(item_name)
for i in range(0, length) :
    index = i
    print(index,"- ", item_name[i], "|   atk :",item_atk[i], "   def :",item_def[i], " ", item_cost[i],"G")

print()
print("구매하고 싶은 아이템의 번호를 입력해주세요")

select = int(input()) # 숫자

# 아이템의 가격 / 내가 소지한 골드

if gold >= item_cost[select] :    
    gold -= item_cost[select]
    print("구매 성공!  남은 골드:",gold,"G")

    target_item = item_name.pop(select)
    target_cost = item_cost.pop(select)
    target_atk = item_atk.pop(select)
    target_def = item_def.pop(select)

    inventory_name.append(target_item)
    inventory_cost.append(target_cost)
    inventory_atk.append(target_atk)
    inventory_def.append(target_def)

else:
    print("골드가 부족합니다")

print("[상점]")
length = len(item_name)
for i in range(0, length) :
    index = i
    print(index,"- ", item_name[i], "|   atk :",item_atk[i], "   def :",item_def[i], " ", item_cost[i],"G")

print()

print("[인벤토리]")
length = len(inventory_name)
for i in range(0, length) :
    index = i
    print(index,"- ", inventory_name[i], "|   atk :",inventory_atk[i], "   def :",inventory_def[i])



# 1. 구매가 가능한지 아닌지 판단
#   불가능하다면 "골드가 부족합니다"

# 2. 가능하다면 구매 진행
# 3. 골드 차감
# 4. 남은 골드 출력

# 5. 인벤토리 배열 추가 - 배열 4개를 이용해 아이템 정보
# 6. 인벤토리 출력

# 7. 상점에서 아이템 삭제


# [인벤토리]
# 0 - 철검  |  atk : 15    def : 0


# 인벤토리
# list <-   인벤토리

# 구매 성공하게 되면 골드를 차감할것

