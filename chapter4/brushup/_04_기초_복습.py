# 문제2. 몬스터(Monster) 클래스
#   속성 - 이름(name), 체력(hp), 주는 경험치(exp)
#   기능 - 등장(appear), 처치 보상(give_exp)
#   인스턴스 3개 : ("슬라임", 40, 5) / ("오크", 120, 20) / ("드래곤", 800, 300)
#   -> 슬라임이(가) 나타났습니다. 체력 40
#   -> 슬라임을(를) 처치해 경험치 5를 얻었습니다.

class Monster : 
    def __init__(self, name, hp, exp):
        self.name= name
        self.hp= hp
        self.exp= exp

    def appear(self):
        print(f"{self.name}이(가) 나타났습니다. 체력 {self.hp}")

    def give_exp(self):
        print(f"{self.name}을(를) 처치해 경험치 {self.exp}를 얻었습니다.")

    def take_damage(self, damage):
        print(f"{self.name}({self.hp})에게 {damage} 피해를 입었습니다.")
        self.hp -= damage
        print(f"남은 체력 : {self.hp}")
    
        


monster_1 = Monster("슬라임", 40, 5)
monster_1.appear()
monster_1.give_exp()

print()

monster_2 = Monster("오크", 120, 20)
monster_2.appear()
monster_2.give_exp()

print()

monster_3 = Monster("드래곤", 800, 300)
monster_3.appear()
monster_3.give_exp()


print()

# 문제3. Monster 클래스 - take_damage(damage) 메서드 추가
#       hp 를 damage 만큼 줄이고 남은 체력을 출력
#       오크(120)에게 30 피해를 세 번
#       -> 오크이(가) 30의 피해를 입었습니다. 남은 체력 90


monster_2.take_damage(20)
monster_2.take_damage(25)
monster_2.take_damage(40)




# 문제4. Monster 를 상속받는 Boss 클래스
#        생성자는 name, hp, exp 에 더해 필살기 이름(skill_name) 을 받는다 (대지 분쇄)
#        부모가 하는 일은 super().__init__(name, hp, exp) 에 맡기고
#				 새로운 기능 - use_skill()
#        -> 고대 골렘이(가) 대지 분쇄을(를) 사용했습니다.

class Boss (Monster):
    def __init__(self, name, hp, exp, skill_name):
        super().__init__(name, hp, exp)        
        self.skill_name = skill_name

    def take_damage(self, damage):
        reduce_damage = damage // 2

        print(f"방어력으로 피해가 절반이 됩니다. {damage} -> {reduce_damage}")
        super().take_damage(reduce_damage)


print()

boss = Boss("고대 골렘", 5000, 1500, "대지 분쇄")
boss.appear()
boss.take_damage(1005)
boss.give_exp()


# 문제5. Boss2 - take_damage 를 다시 정의 [override]
#        보스는 방어력이 높아 받는 피해가 절반으로 줄어든다 (소수점 버림)
#        줄어든 피해량 계산만 하고 실제 체력 계산은 부모 클래스 기능 사용
#        줄어든 피해량 출력
#        -> 방어력으로 피해가 절반이 됩니다. 100 -> 50
#        -> 고대 골렘이(가) 50의 피해를 입었습니다. 남은 체력 250

