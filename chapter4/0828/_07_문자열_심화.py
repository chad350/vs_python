# split / splitlines
code = "WPN-0450-R"  # 무기 코드
code.split('-') # ['WPN', '0450', 'R']
print( " a b c d e".split() ) # ['a', 'b', 'c', 'd', 'e']
print( "a, b, c, d".split(',') ) # ['a', ' b', ' c', ' d']

intro = """안녕하세요.
게임을 시작합니다.

인트로 봐주세요."""
print(intro.splitlines())

# join
item = ["단검", "물약", "갑옷", "로브"]
print("-".join(item))
print(",".join(item))
print(" ".join(item))
print("\n".join(item))


# strip
line = "    Error 에러가 생겼습니다.       "
print(line)
print(line.strip())

line_2 = "#####Error 에러가 생겼습니다.######"
print(line_2)
print(line_2.strip("#"))


# replace
player_hp = "[Chad] hp : 100"
print(player_hp.replace("100", "50"))  # [Chad] hp : 50
print(player_hp.replace("Chad", "Yeom")) # [Yeom] hp : 100
print("a/b/c/d".replace("/"," ")) 


# upper / lower
nickname = "Chad"
print(nickname.upper()) # CHAD
print(nickname.lower()) # chad


# startswith / endswith   -> True / Fals
code = "WPN-0450-R"  # 무기 코드
print(code.startswith("WPN")) # -> 무기가
print(code.endswith("R")) # -> 레어 등급


# find / index / in  문자에서 데이터 확인
code = "WPN-0450-R"  # 무기 코드
print(code in "04") # -> True / False
print(code.index("PN"))  # 문자가 있는지 위치를 확인 / 문자가 없다면?? -> Error 
print(code.find("PEN"))  # 문자가 있는지 위치를 확인 / 문자가 없다면?? -> -1


# isdigit / isaplha / isalnum
print("12345".isdigit())      # 숫자만
print("asdladka".isalpha())   # 문자만
print("asdladka11".isalnum()) # 숫자랑 문자까지