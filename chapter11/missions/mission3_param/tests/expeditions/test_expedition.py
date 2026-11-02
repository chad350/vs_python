import time

import requests

BASE_URL = "https://guild-expedition.fly.dev"


def test_hire_kai(guild):
    response = requests.post(BASE_URL + "/guild/heroes", json={"candidate_id": 3}, headers=guild)
    assert response.status_code == 201, f"카이 고용: 기대 201, 실제 {response.status_code}"
    assert response.json()["remaining_gold"] == 1500, f"남은 골드: 기대 1500, 실제 {response.json()['remaining_gold']}"


def test_rock_cave_power_too_low(guild):
    response = requests.post(BASE_URL + "/guild/heroes", json={"candidate_id": 3}, headers=guild)
    kai_id = response.json()["hero"]["hero_id"]

    response = requests.post(BASE_URL + "/guild/expeditions", json={"dungeon_id": 2, "hero_ids": [kai_id]}, headers=guild)
    assert response.status_code == 403, f"전투력 부족: 기대 403, 실제 {response.status_code}"
    assert response.json()["error_code"] == "POWER_TOO_LOW", f"오류 코드: 실제 {response.json()['error_code']}"


def test_green_forest_in_progress(guild):
    response = requests.post(BASE_URL + "/guild/heroes", json={"candidate_id": 3}, headers=guild)
    kai_id = response.json()["hero"]["hero_id"]

    response = requests.post(BASE_URL + "/guild/expeditions", json={"dungeon_id": 1, "hero_ids": [kai_id]}, headers=guild)
    assert response.status_code == 202, f"원정 접수: 기대 202, 실제 {response.status_code}"
    expedition = response.json()
    assert expedition["status"] == "IN_PROGRESS", f"원정 상태: 실제 {expedition['status']}"
    assert expedition["duration_seconds"] == 2, f"원정 시간: 실제 {expedition['duration_seconds']}"
    expedition_id = expedition["expedition_id"]

    response = requests.post(BASE_URL + f"/guild/expeditions/{expedition_id}/reward", headers=guild)
    assert response.status_code == 409, f"이른 보상: 기대 409, 실제 {response.status_code}"
    assert response.json()["error_code"] == "NOT_COMPLETED"

    response = requests.delete(BASE_URL + f"/guild/heroes/{kai_id}", headers=guild)
    assert response.status_code == 409, f"원정 중 해고: 기대 409, 실제 {response.status_code}"
    assert response.json()["error_code"] == "HERO_ON_EXPEDITION"


def test_green_forest_reward(guild):
    response = requests.post(BASE_URL + "/guild/heroes", json={"candidate_id": 3}, headers=guild)
    kai_id = response.json()["hero"]["hero_id"]

    response = requests.post(BASE_URL + "/guild/expeditions", json={"dungeon_id": 1, "hero_ids": [kai_id]}, headers=guild)
    expedition_id = response.json()["expedition_id"]

    time.sleep(3)
    status = requests.get(BASE_URL + f"/guild/expeditions/{expedition_id}", headers=guild).json()["status"]
    assert status == "COMPLETED", f"원정 상태: 기대 COMPLETED, 실제 {status}"

    response = requests.post(BASE_URL + f"/guild/expeditions/{expedition_id}/reward", headers=guild)
    assert response.status_code == 200, f"보상: 기대 200, 실제 {response.status_code}"
    assert response.json()["gold"] == 1800, f"보상 뒤 골드: 기대 1800, 실제 {response.json()['gold']}"
    assert response.json()["fame"] == 10, f"보상 뒤 명성: 기대 10, 실제 {response.json()['fame']}"

    response = requests.post(BASE_URL + f"/guild/expeditions/{expedition_id}/reward", headers=guild)
    assert response.status_code == 409, f"두 번째 보상: 기대 409, 실제 {response.status_code}"
    assert response.json()["error_code"] == "ALREADY_CLAIMED"
