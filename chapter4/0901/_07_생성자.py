# 생성자
# __init__ 이름
# 첫번째 매개변수로 self 가 있어야 함

class Character : 
    def __init__(self, name, hp, level):
        print("캐릭터가 만들어졌습니다.")
        self.name = name
        self.hp = hp
        self.level = level
        pass


hero = Character("방패 기사", 100, 30)
slime = Character("이끼 슬라임", 40, 10)

print(vars(hero))
print(vars(slime))