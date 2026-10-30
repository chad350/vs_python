import requests
import time

BASE_URL = "https://guild-expedition.fly.dev"

# req
# requests.get(url)
# requests.post(url , header = {} )
# requests.patch(url , params = {} )
# requests.put(url , json = {} )
# requests.delete(url)

# res
# response.status_code <- 
# response.json() <- 
# response.elapsed


# 로그인 → 헤더 → 초기화를 보냅니다.
# POST /auth/token 으로 받은 토큰을 headers 에 넣고, POST /guild/reset 을 보냅니다.
# - 로그인
response = requests.post(f"{BASE_URL}/auth/token", json = {  "username" : "elice_guild"  , "password" : "elice_1234" })
token = response.json()["access_token"]

print("로그인 결과 (auth/token) : ", response.status_code)


headers = {"Authorization" : "Bearer " + token}

# - 초기화
response = requests.post(f"{BASE_URL}/guild/reset", headers=headers)
print("초기화 결과 (guild/reset) : ", response.status_code)


# 세라(후보 5번)를 고용합니다.
# POST /guild/heroes · Body {"candidate_id": 5} · 응답의 hero_id 를 sera_id 에 저장합니다.
response = requests.post(f"{BASE_URL}/guild/heroes", headers=headers, json={ "candidate_id": 5 })
print("세라 고용 결과 (guild/heroes) : ", response.status_code)

sera_id = response.json()["hero"]["hero_id"]


# 던전 2곳의 필요 전투력을 확인합니다.
# GET /dungeons/1 (초록 숲) · GET /dungeons/2 (바위 동굴)
response = requests.get(f"{BASE_URL}/dungeons/1", headers=headers)
print("초록 숲 조회 결과 (dungeons/1) : ", response.status_code)
print("필요 전투력 :", response.json()["required_power"])

response = requests.get(f"{BASE_URL}/dungeons/2", headers=headers)
print("바위 동굴 조회 결과 (dungeons/2) : ", response.status_code)
print("필요 전투력 :", response.json()["required_power"])

# 바위 동굴(2번)에 세라를 보내 봅니다.
# POST /guild/expeditions · Body {"dungeon_id": 2, "hero_ids": [sera_id]} · 403 이 나옵니다.
response = requests.post(f"{BASE_URL}/guild/expeditions", headers=headers, json={ "dungeon_id": 2 , "hero_ids": [sera_id] })
print("바위 동굴 원정 조회 결과 (guild/expeditions : 2) : ", response.status_code)


# 초록 숲(1번)에 세라를 보냅니다.
# Body 의 dungeon_id 를 1로 바꿉니다 · 202 · IN_PROGRESS 가 나오면 expedition_id 를 저장합니다.
response = requests.post(f"{BASE_URL}/guild/expeditions", headers=headers, json={ "dungeon_id": 1 , "hero_ids": [sera_id] })
print("바위 동굴 원정 조회 결과 (guild/expeditions : 1) : ", response.status_code)

# response.json()["status"]
# response.json()["expedition_id"]

if response.json()["status"] == "IN_PROGRESS":
    expedition_id = response.json()["expedition_id"]


# 바로 보상을 요청해 봅니다.
# POST /guild/expeditions/{expedition_id}/reward · 409 NOT_COMPLETED 가 나옵니다.
response = requests.post(f"{BASE_URL}/guild/expeditions/{expedition_id}/reward", headers=headers)
print("원정 보상 결과 (guild/expeditions : 1) : ", response.status_code)


# 원정이 끝날 때까지 1초마다 상태를 조회합니다.
# GET /guild/expeditions/{expedition_id} · status 가 COMPLETED 가 되면 멈춥니다.
# (사용 문법 : for poll_count in range(1, 16): · time.sleep(1) · if status == "COMPLETED": break)
for poll_count in range(1, 16):
    response = requests.post(f"{BASE_URL}/guild/expeditions/{expedition_id}/reward", headers=headers)    
    print(response.json())
    
    if response.status_code == 200:
        break

    time.sleep(1)

print("원정 보상 결과 (guild/expeditions : 1) : ", response.status_code)


# 보상을 받고 길드 정보를 확인합니다.
# 6번과 같은 보상 요청을 다시 보내고, GET /guild 로 골드와 명성을 확인합니다.
response = requests.get(f"{BASE_URL}/guild", headers=headers)
print("길드 정보 조회 결과 (guild) : ", response.status_code)
print("gold :", response.json()["gold"])
print("fame :", response.json()["fame"])
