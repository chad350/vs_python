# 실습1. hero 의 hp 를 80 으로 바꾸고, "def" 키에 5 를 넣고, "mp" 키를 지운 뒤 전체 출력
#       기대 출력: {'name': '루아', 'hp': 80, 'atk': 12, 'def': 5}
hero = {"name": "루아", "hp": 100, "mp": 30, "atk": 12}
hero["hp"] = 80
hero["def"] = 5
del hero["mp"]
print(hero)


# 실습2. hero["luck"] 을 그대로 꺼내 어떤 오류가 나는지 확인
# print(hero["luck"])

# 실습3. 실습2를 오류 없이 기본값 0 이 나오도록 고치고, "luck" 이 있는지 True/False 로 출력
print(hero.get("luck", 0))
print("luck" in hero)

# 실습4. drops 를 순회하며 아이템 개수를 세어 inventory 에 담기
#       if 로 키가 있는지 검사하는 방법과 setdefault 를 쓰는 방법을 모두 써 보고 비교
#       기대 출력: {'포션': 3, '단검': 2, '방패': 1}

inventory = {}
inventory2 = {}
drops = ["포션", "단검", "포션", "방패", "포션", "단검"]

# inventory 딕셔너리를 확인해서
# 지금 item이 없으면
#   -> 새로 딕셔너리에 추가하고 1로 설정
# 지금 item이 있으면
#   -> 딕셔너리에 있는 item 을 1개 추가

for item in drops:
    if item in inventory:
        inventory[item] += 1
    else:
        inventory[item] = 1
print(inventory)

for item in drops:
    inventory2.setdefault(item, 0)
    inventory2[item] += 1
print(inventory2)

base  = {"hp": 100, "atk": 12, "def": 5}
bonus = {"atk": 8, "crit": 0.15}
# 실습5. base 와 bonus 를 update 로 합치고 atk 가 어떻게 되는지 확인한 뒤,
#       기대 출력: {'hp': 100, 'atk': 8, 'def': 5, 'crit': 0.15}

base.update(bonus)
print(base)