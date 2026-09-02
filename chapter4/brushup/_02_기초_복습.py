# 함수 
# 실습1. 인사말을 출력하는 함수 greet() 를 만들고 호출
#       "앨리스 클래스에 오신 것을 환영합니다"

def greet () :
    print("앨리스 클래스에 오신 것을 환영합니다")

greet()


# 실습2. 몬스터 이름을 받아 "OO 을 공격!" 을 출력하는 함수 attack(name) 을 만들고,
#        "슬라임"과 "고블린"으로 두 번 호출

def attack (name) :
    print(f"{name} 을 공격!")


result = attack("슬라임")
attack("고블린")


# 실습3. 숫자를 받아 두 배를 돌려주는 함수 double(n) 을 만들고,
#        double(7) 의 반환값을 변수에 받아서 출력 [return 사용] -> 14

def double(number) :
    return number * 2

double_num = double(7)
print(double_num)


# 실습4. hit(name, damage=10) 처럼 기본값 인자를 두고,
#        damage 없이 한 번 / 30 으로 한 번 호출 [기본값 인자]

def hit(name, damage=10):
    print(f"{name} 가 데미지를 입었습니다   (데미지 : {damage})")

hit("Chad")
hit("Chad", 20)



# 클래스
# 실습6. 이름과 레벨을 속성으로 갖는 Character 클래스를 만들고,
#        이름 : 루아, 레벨 : 3 을 가진 인스턴스를 만들기

class Character :
    def __init__(self, name, level):
        self.name = name
        self.level = level

    def info(self):        
        print(f"{self.name} Lv.{self.level}")

    def change_name(self, name):
        self.name = name

rua  = Character("루아", 3)


# 실습7. 같은 클래스로 "미로", 7 의 데이터를 가진 인스턴스 하나 더 만들기

miro = Character("미로", 7)


# 실습8. rua 의 level 속성을 1 올리고 다시 출력 -> 4
rua.level += 1

# 실습9. Character 클래스에 "루아 Lv.4" 형태로 출력하는 info() 메소드 제작하고 호출
rua.info()
miro.info()

# 실습10. Character 클래스에 닉네임 변경 기능을 추가하고 호출
rua.change_name("new 루아")

print(vars(rua))
print(vars(miro))


# 전투기록 정리 - 리스트와 반복문 연습
damages = [12, 30, 8, 45, 22, 30, 7]

# sum(), max() 사용 금지
# 한 번의 전투에서 기록된 공격 피해량 목록입니다.

# 1) 총 피해량과 평균 피해량을 구해서 출력 
# 2) 30 이상인 데미지가 몇 번인지 세고, 그 값들만 새 리스트 strong_damages 에 모으기
# 3) 최대 피해량을 찾아서 출력
# 4) "N번째 공격: M 피해" 형태로 전체 출력 [enumerate, 번호는 1부터]

# 출력 예제
# -> 총 피해량: 154
# -> 평균 피해량: 22.0
# -> 강타 횟수: 3
# -> 강타 목록: [30, 45, 30]
# -> 최대 피해량: 45
# -> 1번째 공격: 12 피해
# -> 2번째 공격: 30 피해
# -> ...