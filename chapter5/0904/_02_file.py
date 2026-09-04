# 읽기 -> 기존에 파일이 있어야 합니다.
# r

# 쓰기 -> 없어도 새로 만들어요
# w   a   x
f = open("log.txt", "w", encoding="utf-8")
f.write("안녕하세요\n")
f.write("안녕하세요")

f.close()


f = open("log.txt", "r" ,encoding="utf-8")
content = f.read()
f.close()

print(content)


num = 10
name = "chad"
file = open("log.txt")
changed_name = name.replace("c", "d")



# 파일 만들기
# 파일 이름 : test_log.txt
# PASS 로그인 테스트
# PASS 상점 진입 테스트
# FAIL 결제 테스트
# PASS 인벤토리 테스트
# FAIL 우편함 테스트
# PASS 로그아웃 테스트

f = open("test_log.txt", "w", encoding="utf-8")
f.write("PASS 로그인 테스트\n")
f.write("PASS 상점 진입 테스트\n")
f.write("FAIL 결제 테스트\n")
f.write("PASS 인벤토리 테스트\n")
f.write("FAIL 우편함 테스트\n")
f.write("PASS 로그아웃 테스트\n")
f.close()

f = open("test_log.txt", "r" ,encoding="utf-8")

for line in f:
    print("!!! : ",line.rstrip())

f.close()