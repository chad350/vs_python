monsters = ["이끼 슬라임", "동굴 박쥐", "돌 골렘", "탑의 수호자"]
hps      = [30, 60, 150, 400]

# 도감
# 번호를 입력하면 몬스터의 정보를 얻고

# 힌트
def check_monster(idx : int) :
    return ( monsters[idx], hps[idx] )


monster = check_monster( 1 )

print(monster)