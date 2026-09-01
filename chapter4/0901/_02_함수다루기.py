# 중첩해서 함수 생성 가능
def function_1() : 
    def function_2() : 
        pass

    function_2()

function_1()


# 힌트
def greeting(name : str, location : str) : 
    print(f"안녕! 난 {name} 이야")
    print(f"{location}에서 왔어")

# 위치 인자 - ***
greeting("chad", "인천")

# 키워드 인자
greeting(location = "인천", name = "chad")

print()

# 기본값 설정
# 기본값이 없는 매개변수를 먼저 설정
# 기본값이 있는 매개변수는 뒤에 설정
def greeting_global(name, location, home = "한국") : 
    print(f"안녕! 난 {name} 이야")
    print(f"{home}에 있는 {location}에서 왔어")

greeting_global("chad", "인천")
greeting_global("염", "서울")
greeting_global("찬", "강원도", "호주")


# 키워드 전용
def greeting_global_2(name, location, * ,home = "한국") : 
    print(f"안녕! 난 {name} 이야")
    print(f"{home}에 있는 {location}에서 왔어")

greeting_global_2("찬", "강원도", home="미국")


# 가변 인자 - 변수의 갯수를 여러개 받을 수 있게 한다.
def total(*numbers) :    
    print("total :",sum(numbers))
    
total(1,2,3,4,5)






def tmp(name : str = "안녕") :
    pass