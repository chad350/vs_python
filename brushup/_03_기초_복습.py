# 문제1. 무기(Weapon) 클래스
#   속성 - 이름(name), 공격력(damage)
#   기능 - 공격(attack), 정보 출력(info)
#   인스턴스 2개 : ("낡은 검", 12) / ("불꽃 지팡이", 30)
#   -> 낡은 검으로 공격했습니다. 12의 피해를 입혔습니다.
#   -> 무기 이름: 낡은 검 / 공격력: 12

class Weapon :
    def __init__(self, name, damage) :
        self.name = name
        self.damage = damage

    def attack(self):
        print(f"{self.name}으로 공격했습니다. {self.damage}의 피해를 입혔습니다.")

    def info(self):
        print(f"무기 이름: {self.name} / 공격력: {self.damage}")


weapon_1 = Weapon("낡은 검", 12)
weapon_1.attack()
weapon_1.info()

weapon_2 = Weapon("불꽃 지팡이", 30)
weapon_2.attack()
weapon_2.info()


