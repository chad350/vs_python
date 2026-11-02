import requests

BASE_URL = "https://guild-expedition.fly.dev"


def test_hire_arin(guild):
    response = requests.post(BASE_URL + "/guild/heroes", json={"candidate_id": 1}, headers=guild)
    assert response.status_code == 201, f"아린 고용: 기대 201, 실제 {response.status_code}"
    assert response.json()["remaining_gold"] == 2500, f"남은 골드: 기대 2500, 실제 {response.json()['remaining_gold']}"


def test_hire_arin_again(guild):
    response = requests.post(BASE_URL + "/guild/heroes", json={"candidate_id": 1}, headers=guild)
    assert response.status_code == 201, f"아린 고용: 기대 201, 실제 {response.status_code}"
    assert response.json()["remaining_gold"] == 2500, f"남은 골드: 기대 2500, 실제 {response.json()['remaining_gold']}"


def test_not_enough_gold(guild):
    assert requests.post(BASE_URL + "/guild/heroes", json={"candidate_id": 1}, headers=guild).json()["remaining_gold"] == 2500
    assert requests.post(BASE_URL + "/guild/heroes", json={"candidate_id": 3}, headers=guild).json()["remaining_gold"] == 1000

    response = requests.post(BASE_URL + "/guild/heroes", json={"candidate_id": 6}, headers=guild)
    assert response.status_code == 400, f"골드 부족: 기대 400, 실제 {response.status_code}"
    assert response.json()["error_code"] == "NOT_ENOUGH_GOLD"
    assert "보유 1000, 필요 1700" in response.json()["message"], f"메시지: {response.json()['message']}"
