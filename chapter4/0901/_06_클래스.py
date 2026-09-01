class Character : # <- 클래스 (계획서)
    pass


level = 1
num = 10
atk = 15

name = "chad"

mage = Character()    # 인스턴스
mage.job = "마법사"
mage.hp = 80
mage.mp = 30

warrior = Character()   # 인스턴스
warrior.job = "전사"
warrior.hp = 100
warrior.mp = 20



print(vars(mage))



numbers = [1,2,37,23,6,]
numbers.sort()




# 실습1. 내용 없는 Character 클래스 만들기 [pass]
# 실습2. 인스턴스 2개 만들기 [hero, slime]
# 실습3. hero 에 name="방패 기사", hp=100, level=3 속성을 추가
# 실습4. slime 에는 name="이끼 슬라임", hp=30 까지만 속성을 추가 (level X)
#       slime.level 출력 -> 어떤 오류인지 확인

hero = Character()
hero.name = "방패 기사"
hero.hp = 100
hero.level = 3

slime = Character()
slime.name = "이끼 슬라임"
slime.hp = 30

print(slime.level)


# 실습5. Post 클래스도 같은 방법으로 생성 [author, content 를 붙여서 출력]
# author = "Chad"
# content = "점검 안내"

class Post :
    pass

post = Post()
post.author = "Chad"
post.content = "점검 안내"



# 클래스가 없었다면??
# 직업별 능력치
job_list = [ "전사", "도적", "마법사" ]
# hp
hp_list = [ 100, 80 , 70 ]
# mp
mp_list = [ 20, 30 , 50 ]
# 공격력
atk_list = [ 15, 20, 10 ]
# 방어력
defence_list = [ 30, 10, 5 ]






