word = "python"

#   0 1 2 3 4 5
# [ p y t h o n]

# 실습1. 글자 수
print(len(word))
# 실습2. 첫 글자
print(word[0])
# 실습3. 마지막 글자
print(word[-1])
# 실습4. 앞 세 글자
print(word[:3])
# 실습5. 뒤 두 글자
print(word[-2:])
# 실습6. 전부 대문자로
print(word.upper())



fruit = "banana"

# 실습7. a가 몇 개인지
print(fruit.count("a"))
# 실습8. a를 전부 o로 바꾸기
print(fruit.replace("a","o"))
# 실습9. n이 들어 있는지 확인
print("n" in fruit)
# 실습10. n이 처음 나오는 자리
print(fruit.index("n"))
print(fruit.find("n"))


menu = "포션,단검,반지"
items = ["철검", "장검", "대검"]

# 실습11. menu를 쉼표 단위로 잘라서 목록으로 출력 예) 1. 포션  2. 단검  3 반지
tmp = menu.split(",")
for i, m in enumerate(tmp, start=1):
    print(i, ".",m)

# 실습12. items를 ,로 이어 붙여 문자열로  예) 철검,장검,대검
print(",".join(items))


name = "  Hong Gil Dong  "

# 실습13. 양끝 공백 없애기
print(name.strip())

# 실습14. 전부 소문자로 바꾸기
print(name.strip().lower())

# 실습15. 공백을 _ 로 바꾸기
print(name.strip().replace(" ", "_"))


value = "120"
filename = "result.log"

# 실습16. value가 숫자로만 되어 있는지 확인
print(value.isdigit())

# 실습17. 확장자가 log 인지 확인
print(filename.endswith(".log"))


# [선택]

logs = """ERROR 로그인 실패
INFO 접속 성공
ERROR 결제 실패"""

lines = logs.splitlines()           # ["ERROR 로그인 실패", "INFO 접속 성공", "ERROR 결제 실패"]
# 실습18. 행 단위로 나눠서 전체 행 수와 첫 행 출력   -> ERROR 로그인 실패
print("행 수 :", len(lines),  "첫번째 데이터 :", lines[0]) # 행 수 : 3 첫번째 데이터 : ERROR 로그인 실패

# 실습19. ERROR가 몇 번 나오는지
print(logs.count("ERROR"))

# 실습20. 첫 행을 공백으로 잘라서 목록으로          ->['ERROR', '로그인', '실패']
print(lines[0].split())

# 실습21. 첫 행이 ERROR로 시작하는지 확인           
print(lines[0].startswith("ERROR"))