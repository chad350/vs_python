# 람다
# 함수 - 1회용

mail = {"제목": "출석 7일 보상", "골드": 1200}

# 쓸수는 있지만 매번 만들기에는 번거로울수 있다.

#         매개변수
def gold_of( m ):   
    return m["골드"]
#          반환값



# 1. 기본 형식
lambda  매개변수  :  반환값 
gold_of_2 = lambda  m  :  m["골드"] 

# 2. 매개변수 
lambda  :  반환값               # 매개변수 없을 수 있음
lambda  n :  반환값             # 1개가 있을 수 있음
lambda  n, m, z :  반환값       # 여러개가 있을 수 있음
lambda  n, m, z = 10 :  반환값  # 기본값을 설정할 수 있음

# 3. 규칙
# 값을 return 하는 함수라는 것을 전제로 함
# : 뒤에는 반환식을 쓰는데, return 키워드는 생략

# = <- 대입문을 사용할 수 없음
# lambda m : total = m["공드"] XX


# 4. 사용 예시
# 4-1 WebDriveWait 
# until() 에 EC 말고 직접 함수를 제작 가능

# 매개변수 1개가 있어야 하고, 반환값이 bool 인 함수
lambda d : True


# 4-2 
# 정렬이나 최대값/최소값등 기준이 필요한 경우를 설정
mails = [
    {"제목": "출석 7일 보상", "골드": 1200, "만료": 3},
    {"제목": "친구 초대 보상", "골드": 350, "만료": 2},
    {"제목": "시즌 랭킹 보상", "골드": 5000, "만료": 1},
]

# [
# {'제목': '친구 초대 보상', '골드': 350, '만료': 2}, 
# {'제목': '출석 7일 보상', '골드': 1200, '만료': 3}, 
# {'제목': '시즌 랭킹 보상', '골드': 5000, '만료': 1}
# ]
mails_gold = sorted(mails, key= lambda m : m["골드"]  )
print(mails_gold)

# [
# {'제목': '시즌 랭킹 보상', '골드': 5000, '만료': 1}, 
# {'제목': '출석 7일 보상', '골드': 1200, '만료': 3}, 
# {'제목': '친구 초대 보상', '골드': 350, '만료': 2}
# ]
mails_gold = sorted(mails, reverse=True, key= lambda m : m["골드"]  )
print(mails_gold)

# [
# {'제목': '시즌 랭킹 보상', '골드': 5000, '만료': 1},
# {'제목': '친구 초대 보상', '골드': 350, '만료': 2}, 
# {'제목': '출석 7일 보상', '골드': 1200, '만료': 3}
# ]
mails_expire = sorted(mails, key= lambda m : m["만료"]  )
print(mails_expire)


# max(mails, key= lambda m : m["gold"])
# min(mails, key= lambda m : m["gold"])



# Q1. tax_price 와 동일한 기능을 가진 lambda 함수 - tax 를 만들어 보세요.
def tax_price(price):
    return int(price * 1.1)
print(tax_price(1000), tax_price(355))

tax = lambda price : int(price * 1.1)
print(tax(1000), tax(355))


# Q2. 아이템 목록 items 를 가격이 싼 순으로 정렬한 배열을 만들고 출력합니다.
items = [
    {"이름": "강화석", "가격": 1500},
    {"이름": "탈것 상자", "가격": 9900},
    {"이름": "회복 물약", "가격": 300},
]

sorted_items = sorted(items, key= lambda i : i["가격"])
print(sorted_items)

# Q3. 레벨이 가장 높은 플레이어와 레벨이 가장 낮은 플레이어의 닉네임 출력
players = [
    {"닉네임": "달빛기사", "레벨": 52},
    {"닉네임": "별빛궁수", "레벨": 48},
    {"닉네임": "서리방패", "레벨": 61},
]

max_level_player = max(players, key= lambda p : p["레벨"])
min_level_player = min(players, key= lambda p : p["레벨"])

print(f"레벨이 가장 높은 플레이어 : {max_level_player["닉네임"]}")
print(f"레벨이 가장 낮은 플레이어 : {min_level_player["닉네임"]}")


sorted_player = sorted(players, key= lambda i : i["레벨"])
print(f"레벨이 가장 높은 플레이어 : {sorted_player[-1]["닉네임"]}")
print(f"레벨이 가장 낮은 플레이어 : {sorted_player[0]["닉네임"]}")

# 예시
# 레벨이 가장 높은 플레이어 : 서리방패
# 레벨이 가장 낮은 플레이어 : 별빛궁수
