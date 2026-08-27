# 입력받은 숫자가 100 보다큰지 알려주는 프로그램

# 크다면? -> xx 은(는) 100 보다 같거나 큰 수 입니다.
# 작다면? -> xx 은(는) 100 보다 작은 수 입니다.

imput_number = input()
number = int(imput_number)

if number >= 100 :
    print(number, "은(는) 100 보다 같거나 큰 수 입니다.")

else :
    print(number, "은(는) 100 보다 작습니다.")
