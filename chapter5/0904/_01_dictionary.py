#           100  101  200  3  4
numbers = [  1 ,  2 ,  3 , 4 , 5]

# dictioanry
numbers_dict = { 100 : 1, 101 : 2, 200 : 3, 3 : 4}


# Class <- 정보를 가지고 있는 집합
# 플레이어, 아이템, 퀘스트, 친구


# 플레이어
# id
# 닉네임
# 골드
# 길드
# 공격력 / 방어력 / 체력
player = { 
    "nickname" : "chad", 
    "level" : 42,
    "gold" : 2000, 
    "guild" : "엘리스" ,  
    "stat" : { "hp" : 100, "atk" : 20, "def" : 10 }
}


# 플레이어의 레벨
print(player["level"])

# 플레이어의 길드가 있는지 안전하게 확인
print("guild" in player)

# 골드에다가 500 더하기
player["gold"] += 500


# 정보 체크
print(player["nickname"])   # 있는 정보에 접근
print(player.get("job"))    # 있던/없던 정보를 읽는것
print("job" in player)      # 있는지 없는지 확인

# 정보 추가
player["nickname"] = "채드"    # 있는 데이터를 수정
player["job"] = "법사"         # 없을때 사용하면 데이터를 추가
player.setdefault("job", "전사")    # 있는 데이터라면 설정하지 X
player.setdefault("ranking", 100)  # 없는 데이터라면 섫정

# 정보 삭제
del player["job"]



# 이름
# 등급
# 수치 [ value - 공격력 / 방어력 / 회복량 ]

# 강철검      rare       45 
# 용사의 방패  legend     80
# 회복물약     common    100

# item
item = { "name" : "강철검" , "grade" : "rare" , "value" : 45  }
item2 = { "name" : "용사의 방패" , "grade" : "legend" , "value" : 80  }
item3 = { "name" : "강철회복물약검" , "grade" : "common" , "value" : 100  }

# inventory
inventory = {
    "slot_1" : { "name" : "강철검" , "grade" : "rare" , "value" : 45  },
    "slot_2" : { "name" : "용사의 방패" , "grade" : "legend" , "value" : 80  },
    "slot_3" : { "name" : "강철회복물약검" , "grade" : "common" , "value" : 100  }
}

print(item["name"])
print(inventory["slot_2"]["grade"])



# 친구 정보 <-   
# id
# 닉네임
# 접속상태인지
# 친구 레벨
friends = [
    {"player_id": "P10091", "nickname": "은빛여우", "status": "online", "friendship_level": 5},
    {"player_id": "P10456", "nickname": "철벽수호자", "status": "offline", "friendship_level": 3},
    {"player_id": "P10789", "nickname": "바람의검객", "status": "online", "friendship_level": 8},
]


# 첫번째 친구의 이름을 확인    "nickname"
# friends[0]
# #{"player_id": "P10091", "nickname": "은빛여우", "status": "online", "friendship_level": 5},
print(friends[0]["nickname"])

# 세번째 친구의 접속상태를 확인  "status"
# friends[2]
# {"player_id": "P10789", "nickname": "바람의검객", "status": "online", "friendship_level": 8},
print(friends[2]["status"])

names = ["chad", "연", "찬"]
# 0 {"player_id": "P10091", "nickname": "은빛여우", "status": "online", "friendship_level": 5},\
# 1 {"player_id": "P10456", "nickname": "철벽수호자", "status": "offline", "friendship_level": 3},
# 2 {"player_id": "P10789", "nickname": "바람의검객", "status": "online", "friendship_level": 8},
for friend in friends:
    print(friend["nickname"])

request_friend_delete = {
   "friend_id" : "P10091"
}

# request_friend_delete["friend_id"]
delete_id = request_friend_delete["friend_id"]
for friend in friends:
    if friend["player_id"] == delete_id : 
        print(f"{friend["nickname"]}를 친구에서 삭제합니다.")


guild = {
    "guild_id": "G0007",
    "name": "새벽의 등불",
    "level": 12,
    "members": [
        {"player_id": "P10234", "nickname": "달빛기사", "role": "leader", "equipped": {"weapon": "IT1001", "shield": "IT1003"}},
        {"player_id": "P10091", "nickname": "은빛여우", "role": "member", "equipped": {"weapon": "IT1002", "shield": None}},
    ],
}

# guild["guild_id"]
# guild["name"]
# guild["level"]

# 정보가 2개상 -> list -> for

# for : 반복 -> 2개 이상 체크

# if : 조건문
# 5명의 정보가 있을때 -> 무조건 다 실행
# 5명면이 있을때 레벨이 10 이상인 사람, (조건)

members = guild["members"]
for m in members:
    # m["role"] 확인
    # m["nickname"] 확인
        
    if m["role"] == "leader":
        print(f"{m["nickname"]}는 리더입니다.")