import _02_함수_매개변수

# 저장하지 못한다
# print("test")

# 함수의 결과를 저장한다
# num = len("123456")
# print(num)

def intput_number() : 
    input_number = input()
    number = int(input_number)

    return number

print()
print("두배로 출력할 수 를 입력해주세요.")


num1 = intput_number()
_02_함수_매개변수.double(num1)


print()

print("더하기 할 수를 입력해주세요 (1/2)")
num2 = intput_number()

print("더하기 할 수를 입력해주세요 (2/2)")
num3 = intput_number()
_02_함수_매개변수.add(num2, num3)