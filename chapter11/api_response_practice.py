import requests

BASE_URL = "https://guild-expedition.fly.dev"

# - 로그인
print("\n1. 로그인하고 길드 정보를 초기화합니다")

response = requests.post(f"{BASE_URL}/auth/token", json = {  "username" : "elice_guild"  , "password" : "elice_1234" })
token = response.json()["access_token"]
print("로그인 - 결과 기대 결과 - 200 : 실제 결과 :", response.status_code)

headers = {"Authorization" : "Bearer " + token}

# - 초기화
response = requests.post(f"{BASE_URL}/guild/reset", headers=headers)
print("로그인 - 결과 기대 결과 : 200 - 실제 결과 :", response.status_code)


print("\n2. 바른(후보 2번) · 세라(후보 5번)를 고용")
# POST /guild/heroes 를 2번 보내고, 응답의 hero_id 를 변수 barun_id · sera_id 에 저장합니다.

response = requests.post(f"{BASE_URL}/guild/heroes", headers=headers, json = {  "candidate_id" : 2})
barun_id = response.json()["hero"]["hero_id"]

print("2번 후보 고용 - 결과 기대 결과 : 201 - 실제 결과 :", response.status_code)
print("barun_id :", barun_id)

response = requests.post(f"{BASE_URL}/guild/heroes", headers=headers, json = {  "candidate_id" : 5})
sera_id = response.json()["hero"]["hero_id"]

print("5번 후보 고용 - 결과 기대 결과 : 201 - 실제 결과 :", response.status_code)
print("sera_id :", sera_id)


print("\n3. 상점에서 강철 검(102) · 불꽃 지팡이(103) 를 1개씩 주문")
response = requests.post(f"{BASE_URL}/guild/orders", headers=headers, json = {  "item_id" : 102 , "quantity" : 1})
print("102 아이템 구매 - 결과 기대 결과 : 201 - 실제 결과 :", response.status_code)

response = requests.post(f"{BASE_URL}/guild/orders", headers=headers, json = {  "item_id" : 103 , "quantity" : 1})
print("103 아이템 구매 - 결과 기대 결과 : 201 - 실제 결과 :", response.status_code)


print("\n4. 바른에게 강철 검을 장착")
response = requests.put(f"{BASE_URL}/guild/heroes/{barun_id}/equipment", headers=headers, json = { "weapon" : 102, "armor" : None})
print("바른 무기 장착 - 결과 기대 결과 : 200 - 실제 결과 :", response.status_code)

print("\n5. 세라에게 불꽃 지팡이를 장착")
response = requests.patch(f"{BASE_URL}/guild/heroes/{sera_id}/equipment", headers=headers, json = { "weapon" : 103})
print("세라 무기 장착 - 결과 기대 결과 : 200 - 실제 결과 :", response.status_code)


print("\n6. 골드가 모자란 상태에서 가죽 갑옷(201) 을 주문 후 결과 검증 - status code, gold")
response = requests.post(f"{BASE_URL}/guild/orders", headers=headers, json = {  "item_id" : 201 , "quantity" : 1})
print("201 아이템 구매 - 결과 기대 결과 : 400 - 실제 결과 :", response.status_code)

response = requests.get(f"{BASE_URL}/guild", headers=headers)
print("남은 작액 기대 결과 : 100 - 실제 결과", response.json()["gold"])


print("\n7. 길드 정보 · 창고 · 영웅 목록 · 던전 2 을 조회")

response = requests.get(f"{BASE_URL}/guild/storage", headers=headers)
guild_storage = response.json()["items"]
print(guild_storage)


response = requests.get(f"{BASE_URL}/guild/heroes", headers=headers)
guild_total_power = 0
for hero in response.json()["items"]: 
    guild_total_power += hero["total_power"]
    

response = requests.get(f"{BASE_URL}/dungeons/2", headers=headers)
required_power = response.json()["required_power"]

print(f"길드의 전투력 : {guild_total_power} / 던전의 필요 전투력 : {required_power}")