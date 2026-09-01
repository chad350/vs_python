# 실습10. Character 클래스에 생성자 만들고 name, hp, level 속성 추가 - 매개 변수 X
# name : "Chad"
# hp : 100
# level : 10
class Character:
    def __init__(self):
        self.name = "chad"
        self.hp = 100
        self.level = 10

character1 = Character()
print(vars(character1))



# 실습11. Character2 클래스에 생성자 만들고 name, hp, level 를 인자로 전달 할 수 있도록 생성
# 실습12. 인스턴스 2개를 만들어 name 과 hp 출력

class Character2 : 
    def __init__(self, name ,hp ,level ):
        self.name = name
        self.hp = hp
        self.level = level

slime = Character2("슬라임", 40, 2)
orc = Character2("오크", 120, 5)

print(vars(slime))
print(vars(orc))