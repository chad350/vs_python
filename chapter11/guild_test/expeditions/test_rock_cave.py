import pytest
import requests
import time

BASE_URL = "https://guild-expedition.fly.dev" 


def test_rock_cave_first_expedition( guild_auth ):
    # 카이(3) · 세라(5)를 고용    
    # POST /guild/heroes

    response = requests.post(f"{BASE_URL}/guild/heroes", json={ "candidate_id" : 3 }  , headers=guild_auth)
    assert response.status_code == 201
    kai_id = response.json()["hero"]["hero_id"]

    response = requests.post(f"{BASE_URL}/guild/heroes", json={ "candidate_id" : 5 }  , headers=guild_auth)
    assert response.status_code == 201
    sera_id = response.json()["hero"]["hero_id"]

    # 잔액 확인
    assert response.json()["remaining_gold"] == 500



    # 강철 검(102)을 주문
    # POST /guild/orders
    response = requests.post(f"{BASE_URL}/guild/orders", json={ "item_id":102, "quantity" : 1  }, headers=guild_auth)
    print(response.json())
    assert response.status_code == 201
    assert response.json()["remaining_gold"] == 100


    # 카이에게 장착
    # PATCH /guild/heroes/{kai_id}/equipment
    # json {"weapon": 102}
    response = requests.patch(f"{BASE_URL}/guild/heroes/{kai_id}/equipment", json={ "weapon": 102 }, headers=guild_auth)
    assert response.status_code == 200
    assert response.json()["total_power"] == 310


    # 바위 동굴(던전 2)로 원정
    # POST /guild/expeditions · json {"dungeon_id": 2, "hero_ids": [kai_id, sera_id]}
    response = requests.post(f"{BASE_URL}/guild/expeditions", json={ "dungeon_id" : 2 ,   "hero_ids" : [ kai_id, sera_id ]  }, headers=guild_auth)
    assert response.status_code == 202
    assert response.json()["party_power"] == 510

    expedition_id = response.json()["expedition_id"]
 
    # 원정 중인 세라를 해고
    # DELETE /guild/heroes/{sera_id}
    response = requests.delete(f"{BASE_URL}/guild/heroes/{sera_id}", headers=guild_auth)
    assert response.status_code == 409
    assert response.json()["error_code"] == "HERO_ON_EXPEDITION"


    # 원정 중 3초 대기
    time.sleep(3)

    # 원정 상태를 1번 조회
    response = requests.get(f"{BASE_URL}/guild/expeditions/{expedition_id}", headers=guild_auth)
    assert response.status_code == 200
    assert response.json()["status"] == "COMPLETED"

    # 보상을 요청 
    response = requests.post(f"{BASE_URL}/guild/expeditions/{expedition_id}/reward", headers=guild_auth)
    assert response.status_code == 200
    assert response.json()["gold_reward"] == 700
    assert response.json()["fame_reward"] == 25

    # 길드 정보를 조회
    response = requests.get(f"{BASE_URL}/guild", headers=guild_auth)
    assert response.status_code == 200
    assert response.json()["gold"] == 800
    assert response.json()["fame"] == 25