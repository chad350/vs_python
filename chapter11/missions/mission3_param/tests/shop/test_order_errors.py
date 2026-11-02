import pytest
import requests

BASE_URL = "https://guild-expedition.fly.dev"


# TODO 1 · 케이스 표 CASES 와 결과 이름 CASE_IDS
CASES = []
CASE_IDS = []


# TODO 2 · parametrize 데코레이터 (인자 이름 4개 · CASES · ids=CASE_IDS)
def test_order_error_cases(guild, name, body, status, error_code):
    response = requests.post(BASE_URL + "/guild/orders", json=body, headers=guild)
    assert response.status_code == status, f"{name}: 기대 {status}, 실제 {response.status_code}"
    assert response.json()["error_code"] == error_code, f"{name}: 기대 {error_code}, 실제 {response.json()['error_code']}"


def test_duplicate_order_key(guild):
    response = requests.post(BASE_URL + "/guild/orders", json={"item_id": 101, "quantity": 1, "order_key": "k-001"}, headers=guild)
    assert response.status_code == 201, f"첫 주문: 기대 201, 실제 {response.status_code}"

    response = requests.post(BASE_URL + "/guild/orders", json={"item_id": 101, "quantity": 1, "order_key": "k-001"}, headers=guild)
    assert response.status_code == 409, f"같은 키 재주문: 기대 409, 실제 {response.status_code}"
    assert response.json()["error_code"] == "DUPLICATE_ORDER_KEY"
