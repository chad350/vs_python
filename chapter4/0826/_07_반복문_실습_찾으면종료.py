
numbers = [10, 5, 23, 60, 33, 65, 2, 90, 86]

# 60 을 찾으면 for 바로 종료하고 60이 몇번째에 있는지 print
# 60을 찾았다 - n 번째에 있었다.

# idx = 0
# for i in numbers :    
#     idx+=1
#     if i == 60 :
#         print(i,"을 찾았습니다 - idx :", idx)
#         break

leng = len(numbers)
for i in range(leng) :    
    num = numbers[i]

    if num == 60 :
        print(num,"을 찾았습니다 - idx :", i +1)
        break