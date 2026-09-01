import math

# dir
# help
print(dir(math))
help(math)
help(math.log)



print(math.log(1000, 72))
#              진수   밑수

from math import log
log()

from math import log, ceil, degrees

# 별칭
from math import log as l
l()

from math import pi as our_pi
print(our_pi)


import _01_fstring
import _02_함수다루기

# 패키지를 통한 접근
import tmp.t




# 플레이어   hp
# 몬스터    hp
# from player import hp as player_hp
# from monster import hp as monster_hp

# print(player_hp)


import random

# 숫자 - 랜덤
print(random.random())  # 0.0 이상 / 1.0 미만의 실수
print(random.random() * 100)
print(random.uniform(0, 10)) # a 이상 b 이하 - 실수
print(random.randint(10, 20))  # a 이상 b 이하 - 정수
print(random.randrange(0, 100))  # a 이상 b 미만 - 정수


items = [ "물약", "물약", "물약", "물약", "낡은 단검", "가죽", "100G"]
print(random.choice(items)) # 시퀀스에 있는 아이템을 하나 랜덤으로 선택

random.shuffle(items)
print(items)
