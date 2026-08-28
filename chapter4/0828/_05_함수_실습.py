# 실습1. 두 수를 받아 뺀것을 출력하는 함수
def minus( num_1, num_2) :
    print( num_1 - num_2)

minus(1, 5)


# 실습2. 이름을 받아 "환영합니다, OO님" 을 출력만 하는 함수
def greeting(name) : 
    print("환영합니다,", name  , "님")

player_name = input()
greeting(player_name)


monsters = ["이끼 슬라임", "동굴 박쥐", "돌 골렘", "탑의 수호자"]
hps      = [30, 60, 150, 400]

# 실습3. 번호를 입력하면 몬스터의 이름과 가격을 출력하는 함수 
def print_monster_info ( idx ) :
    monster_name = monsters[idx]
    monster_hp = hps[idx]

    print(monster_name, monster_hp)

print_monster_info(1)


# 실습4. 번호를 입력하면 몬스터의 이름을 반환하는 함수
def get_monster_name(idx) :
    monster_name = monsters[idx]
    return monster_name

monster_name = get_monster_name(2)
print(monster_name)