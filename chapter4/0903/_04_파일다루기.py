text = 't'
print(ord('a'))
print(ord('A'))

# 문자를 숫자로 저장할때의 규칙
# 인코딩
# utf-8 / cp949

print("글자 길이")
print(len("Hi"))
print(len("안녕"))

print("크기(용량) 확인")
print(len("Hi".encode("utf-8")))
print(len("안녕".encode("utf-8")))
print(len("안녕".encode("cp949")))



# r - 읽기 : 파일이 있는 상태에 실행가능, 없으면 에러
# w - 쓰기 : 파일이 없으면 생성, 있으면 기존 파일 사용, 기존 내용을 다 삭제하고 새로 글을 씀
# a - 쓰기 : 파일이 없으면 생성, 있으면 기존 파일 사용, 기존 내용 뒤에가사 글을 추가
# x - 쓰기(베타적) : 파일이 없으면 생성, 있으면 에러

# open 시 지정하는 옵션은 2가지
# mode
# encoding
f = open("text.txt", "a", encoding="utf-8")
f.write("Hi")
f.close()

# read()
# readline()
# readlines()

# write()
# writeliens()

# tell
# seek




f = open("text.txt", encoding="uft-8")
f.close()

with open("text.txt", encoding="uft-8") as f:
    f.read()


    