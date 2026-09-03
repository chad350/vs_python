# 이후에 수정이 가능
hero = {"name": "루아", "job": "궁수", "level": 12}

# 데이터 접근하기
print(hero["name"]) # 있는 데이터는 접근 가능
# print(hero["gold"]) # 없데이터 데이터는 접근시 에러

# 데이터 체크
print("name" in hero)
print("gold" in hero)

# 기본값 체크
print(hero.get("name", "noname"))
print(hero.get("gold", 0))

# 기본값 설정
hero.setdefault("name", "미로")
hero.setdefault("hp", 100)


# 딕셔너리 합치기
# 중복되는 키값이 덮어쓰기가된다 (원본이 사라짐)
stat = { "level" : 20, "mp" : 30, "atk" : 15, "def" : 5}
hero.update(stat)

print(hero)


