number = [2, 5, 29, 20, 80, 90, 52, 80]

# 2, 5, 29, 20, 80, 90, 52, 80
print("test_1")
for num in number :
    print(num)

# 0 - 9
print("test_2")
for i in range(10) :
    print(i)

# 5 - 9
print("test_3")
for i in range(5, 10) :
    print(i)

# 1, 3, 5, 7, 9
print("test_4")
for i in range(1, 10, 1) :
    print(i)

# enumerate
items = ["포션", "스크롤", "재료템"]

for idx, item in enumerate(items) : 
    print(idx, item)

for idx, item in enumerate(items, start = 1) : 
    print(idx, item)


# zip
item_name = ["철검", "연습용 검", "연습용 방패", "나무 지팡이"        ]
item_cost = [100,       150,          130,          200      ]
item_atk  = [15,          5,            0,           20      ]
item_def  = [0,           0,            5,           0       ]

for name, atk, defence, cost in zip(item_name, item_atk, item_def, item_cost):
    print(name, atk, defence, cost)