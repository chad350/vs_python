import time

import pytest
import requests

BASE_URL = "https://guild-expedition.fly.dev"


@pytest.mark.expedition
def test_rock_cave_first_expedition(guild):

    response = requests.post(BASE_URL + "/guild/heroes", json={"candidate_id": 3}, headers=guild)
    assert response.status_code == 201, f"카이 고용: 기대 201, 실제 {response.status_code}"
    kai_id = response.json()["hero"]["hero_id"]
    response = requests.post(BASE_URL + "/guild/heroes", json={"candidate_id": 5}, headers=guild)
    assert response.status_code == 201, f"세라 고용: 기대 201, 실제 {response.status_code}"
    assert response.json()["remaining_gold"] == 500, f"고용 뒤 골드: 기대 500, 실제 {response.json()['remaining_gold']}"
    sera_id = response.json()["hero"]["hero_id"]

    response = requests.post(BASE_URL + "/guild/orders", json={"item_id": 102, "quantity": 1}, headers=guild)
    assert response.status_code == 201, f"강철 검 주문: 기대 201, 실제 {response.status_code}"
    assert response.json()["remaining_gold"] == 100, f"주문 뒤 골드: 기대 100, 실제 {response.json()['remaining_gold']}"
    response = requests.patch(BASE_URL + f"/guild/heroes/{kai_id}/equipment", json={"weapon": 102}, headers=guild)
    assert response.json()["total_power"] == 310, f"카이 총 전투력: 기대 310, 실제 {response.json()['total_power']}"

    response = requests.post(BASE_URL + "/guild/expeditions", json={"dungeon_id": 2, "hero_ids": [kai_id, sera_id]}, headers=guild)
    assert response.status_code == 202, f"원정 접수: 기대 202, 실제 {response.status_code}"
    assert response.json()["party_power"] == 510, f"파티 전투력: 기대 510, 실제 {response.json()['party_power']}"
    expedition_id = response.json()["expedition_id"]

    response = requests.delete(BASE_URL + f"/guild/heroes/{sera_id}", headers=guild)
    assert response.status_code == 409, f"원정 중 해고: 기대 409, 실제 {response.status_code}"
    assert response.json()["error_code"] == "HERO_ON_EXPEDITION"

    time.sleep(3)
    status = requests.get(BASE_URL + f"/guild/expeditions/{expedition_id}", headers=guild).json()["status"]
    assert status == "COMPLETED", f"원정 상태: 기대 COMPLETED, 실제 {status}"

    response = requests.post(BASE_URL + f"/guild/expeditions/{expedition_id}/reward", headers=guild)
    assert response.status_code == 200, f"보상: 기대 200, 실제 {response.status_code}"
    assert response.json()["gold"] == 800, f"보상 뒤 골드: 기대 800, 실제 {response.json()['gold']}"
    assert response.json()["fame"] == 25, f"보상 뒤 명성: 기대 25, 실제 {response.json()['fame']}"

    data = requests.get(BASE_URL + "/guild", headers=guild).json()
    assert data["gold"] == 800, f"길드 골드: 기대 800, 실제 {data['gold']}"
    assert data["fame"] == 25, f"길드 명성: 기대 25, 실제 {data['fame']}"
