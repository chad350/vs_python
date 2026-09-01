# 생성자
# __init__ 이름
# 첫번째 매개변수로 self 가 있어야 함

class Character : 
    def __init__(self, name, hp, level):
        print("캐릭터가 만들어졌습니다.")
        self.name = name
        self.hp = hp
        self.level = level

    # 자기소개
    def introduce(self):
        print(f"안녕하세요 제 이름 {self.name} 입니다. 레벨은 {self.level}입니다.")

    # 레벨업
    def level_up(self):
        self.level += 1

    # 피격


hero = Character("방패 기사", 100, 30)
slime = Character("이끼 슬라임", 40, 10)



# 학생 [클래스]

# 속성 [정보들]
# 이름, 학년, 학교, 핸드폰(모델, 전화번호, 색), 친구

# 메서드 [행동들]
# 자기소개, 전화기 자랑, 친구 추가, 친구 삭제, 학년업

class Student :
    def __init__(self, name, grade, school):
        self.name = name
        self.grade = grade
        self.school = school
        self.phone = "핸드폰"
        self.friend = []

    def introduce(self):
        print(f"안녕 내이름은 {self.name}야")

    def change_name(self, name):
        if 0 < len(name) < 6 : 
            self.name = name

    def add_friend(self, name):
        if name in self.friend:
            return            
        self.friend.append(name)      

    def remove_friend(self, name):
        if name in self.friend:
            self.friend.remove(name)

    def level_up(self):
        self.grade += 1

    

student_1 = Student("Chad", 15, "앨리스 대학원")
student_1.introduce()
student_1.change_name("염dklasjdlkasjdlk씨")
student_1.introduce()

student_1.add_friend("찬씨")
student_1.add_friend("염예씨")
student_1.add_friend("찬씨")

print(vars(student_1))




student_2 = Student("찬씨", 10, "앨리스 대학교")





