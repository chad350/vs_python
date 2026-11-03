import requests
import time

BASE_URL = "https://guild-expedition.fly.dev" 
USERNAME = "elice_chad"
PASSWORD = "elice_1234"

# 테스트 1
# 용병을 고용 하는 테스트
def test_hire():
    # 로그인 - 토큰 획득
    response = requests.post(f"{BASE_URL}/auth/token", json={ "username":USERNAME , "password":PASSWORD })
    
    token = response.json()["access_token"]

    # 토큰 정보를 헤더에 저장
    h = { "Authorization" : f"Bearer {token}"}

    # 테스트 전에 길드정보 초기화 
    requests.post(f"{BASE_URL}/guild/reset" , headers=h)

    # 고용 - 3번 후보
    response = requests.post(f"{BASE_URL}/guild/heroes", json={ "candidate_id" : 3 }, headers=h)

    # 테스트
    # 원하는 동작이 잘 이루어졌는지
    # 데이터를 검증 : 원하는 값이 들어왔는지 보는 것
    # 상태 코드 : 201
    # 남은 골드 : 1500
    assert response.status_code == 201, f"[3번 후보 고용] 기대 결과 201, 실제 결과 {response.status_code}"
    assert response.json()["remaining_gold"] == 1500, f"[고용 후 잔액] 기대 결과는 1500, 실제 결과 {response.json()['remaining_gold']}"




# 테스트 2 
# 고용한 용병을 원정을 보내는 요청
# 용병 전투력 260 / 원정 대상의 전투력 450 
# 전투력이 부족한 상황에 대해서 검증
def test_expidetion_to_cave():

    # 테스트 1 번의 내용 - 고용하는 것 까지 확인
    response = requests.post(f"{BASE_URL}/auth/token", json={ "username":USERNAME , "password":PASSWORD })
    token = response.json()["access_token"]
    h = { "Authorization" : f"Bearer {token}"}
    
    requests.post(f"{BASE_URL}/guild/reset" , headers=h)

    response = requests.post(f"{BASE_URL}/guild/heroes", json={ "candidate_id" : 3 }, headers=h)
    hero_id = response.json()["hero"]["hero_id"]

    # 원정을 요청 -> 실패
    # 전투력이 부족
    # 던전 id 2
    # 영웅 id 1
    response = requests.post(f"{BASE_URL}/guild/expeditions", json={ "dungeon_id": 2, "hero_ids":[hero_id] } , headers=h)

    # 테스트 결과
    # 상태 코드 : 403
    # 에러 코드 : POWER_TOO_LOW
    assert response.status_code == 403
    assert response.json()["error_code"] == "POWER_TOO_LOW"



# 테스트 3 
# 던전 2가지 
#  1번 던전 : O <- 원정 보내는 
#  2번 던전 : X
# O 원정을 보내는 것 
# X 아직 끝나지 않았는데 보상 수령 요청 
# X 원정 중인 대상을 해고 
def test_expidetion_to_forest():

    # 테스트 1 번의 내용
    response = requests.post(f"{BASE_URL}/auth/token", json={ "username":USERNAME , "password":PASSWORD })
    token = response.json()["access_token"]
    h = { "Authorization" : f"Bearer {token}"}
    
    requests.post(f"{BASE_URL}/guild/reset" , headers=h)

    response = requests.post(f"{BASE_URL}/guild/heroes", json={ "candidate_id" : 3 }, headers=h)
    hero_id = response.json()["hero"]["hero_id"]

    # 테스트 2 번의 내용
    # dungeon_id 만 1번으로 요청
    response = requests.post(f"{BASE_URL}/guild/expeditions", json={ "dungeon_id": 1, "hero_ids":[hero_id] } , headers=h)

    # 원정 검증 결과 202 
    assert response.status_code == 202

    expedition_data = response.json()

    assert expedition_data["status"] == "IN_PROGRESS"
    assert expedition_data["remaining_seconds"] == 2
    assert expedition_data["duration_seconds"] == 2

    expedition_id = expedition_data["expedition_id"]

    # 보상을 요청 (IN_PROGRESS 인 상태) <- 테스트
    response = requests.post(f"{BASE_URL}/guild/expeditions/{expedition_id}/reward", headers=h)

    # 상태 코드 : 409
    # 에러 코드 : NOT_COMPLETED
    assert response.status_code == 409
    assert response.json()["error_code"] == "NOT_COMPLETED"

    # 영웅 해고 <- 원정 중인 대상
    response = requests.delete(f"{BASE_URL}/guild/heroes/{hero_id}", headers=h)
    # 상태 코드 : 409
    # 에러 코드 : HERO_ON_EXPEDITION
    assert response.status_code == 409
    assert response.json()["error_code"] == "HERO_ON_EXPEDITION"


def test_expidetion_to_forest_complete():
    # 테스트 1 번의 내용
    response = requests.post(f"{BASE_URL}/auth/token", json={ "username":USERNAME , "password":PASSWORD })
    token = response.json()["access_token"]
    h = { "Authorization" : f"Bearer {token}"}
    
    requests.post(f"{BASE_URL}/guild/reset" , headers=h)

    response = requests.post(f"{BASE_URL}/guild/heroes", json={ "candidate_id" : 3 }, headers=h)
    hero_id = response.json()["hero"]["hero_id"]

    # 테스트 2 번의 내용
    response = requests.post(f"{BASE_URL}/guild/expeditions", json={ "dungeon_id": 1, "hero_ids":[hero_id] } , headers=h)
    expedition_data = response.json()
    expedition_id = expedition_data["expedition_id"]

    # 원정이 끝나는 것(2초) 을 대기
    time.sleep(3)


    # 대기를 하고 나서 원정 상황을 체크
    response = requests.get(f"{BASE_URL}/guild/expeditions/{expedition_id}", headers=h)

    # 상태 코드 : 200
    # status : COMPLETED
    assert response.status_code == 200
    assert response.json()["status"] == "COMPLETED"


    # 테스트 3 번의 내용 - 보상 요청
    response = requests.post(f"{BASE_URL}/guild/expeditions/{expedition_id}/reward", headers=h)

    # 상태 코드 : 200
    # 원정의 보상 골드 : 
    # 길드의 총 골드
    # 원정의 보상 명예 : 
    # 길드의 총 명예

    reward_data = response.json()

    assert response.status_code == 200
    assert reward_data["gold_reward"] == 300
    assert reward_data["fame_reward"] == 10
    assert reward_data["gold"] == 1800
    assert reward_data["fame"] == 10


    # 보상이 이미 받아졌는데 -> 또 보상을 요청 : 실채
    response = requests.post(f"{BASE_URL}/guild/expeditions/{expedition_id}/reward", headers=h)

    # 상태 코드 : 409
    # 에러 코드 : ALREADY_CLAIMED
    assert response.status_code == 409
    assert response.json()["error_code"] == "ALREADY_CLAIMED"
    
    # 영웅 해고
    response = requests.delete(f"{BASE_URL}/guild/heroes/{hero_id}", headers=h)

    # 상태 코드 : 204
    assert response.status_code == 204