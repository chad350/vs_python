# 짝수인지 / 홀수인지
# 수가 짝수라면 - “xx 은(는) 짝수 입니다.”
# 수가 홀수라면 - “xx 은(는) 홀수 입니다.”

# 2로 나누어서 "나머지" -> 0 짝수, 1이면 홀수

imput_number = input()
number = int(imput_number)

remain = number % 2
is_odd = remain == 1

if is_odd : 
    print (number, "은(는) 홀수 입니다.")
else :
    print (number, "은(는) 짝수 입니다.")