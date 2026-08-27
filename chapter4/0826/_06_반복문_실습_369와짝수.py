numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

for num in numbers : 
    remain = num % 3
    
    if remain == 0 :
        print("짝")
    else :
        print(num)

print()


# 짝수인 것만 출력되도록
for num in numbers : 
    remain = num % 2

    if remain == 1 :
        continue

    print(num)

