# 자료형
number = 10       # 숫자      int
exp = 56.4        # 소수점     float
name = "Chad"     # 문자      str
has_item = False  # 참 / 거짓  bool

# 여러개의 데이터
# 순서에 따라 접근 시퀀스

#               0       1      2
monsters    = ["오크", "슬라임", "드래곤"]    # list
bag         = ["물약", "물약"  , "단검"]     # list - 중복 허용 O

equip       = ["장검",  "방패"]             # set  - 중복 허용 X

weapon      = ("낡은 창",  10 ,  500)       # tuple - 만들어지고 수정 불가

print(monsters[0])
print(bag[2])
print(equip[1])
print(weapon[0])


print()
# 방에
# 3가지

# 101    - 염씨
# 304    - 예씨
# 1006   - 찬씨
#           101   304    1006
friends = ["염씨", "예씨", "찬씨"]

# 딕셔너리
friends_dic = { 101 : "염씨", 304 : "예씨", 1006 :"찬씨"   }
print(friends_dic[101])
print(friends_dic[304])
print(friends_dic[1006])

print()

# 문자를 키워드
game_rule = { "name" : "card", "time" : 60, "player" : 5 }
print(game_rule["name"])
print(game_rule["time"])
print(game_rule["player"])






