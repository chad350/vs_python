import pytest
import requests

BASE_URL = "https://guild-expedition.fly.dev"


# 1	("없는 아이템", {"item_id": 999, "quantity": 1}, 404, "ITEM_NOT_FOUND")	"item_not_found"
# 2	("수량 0", {"item_id": 101, "quantity": 0}, 422, "INVALID_QUANTITY")	"quantity_zero"
# 3	("수량 100", {"item_id": 101, "quantity": 100}, 422, "INVALID_QUANTITY")	"quantity_100"
# 4	("골드 부족", {"item_id": 103, "quantity": 99}, 400, "NOT_ENOUGH_GOLD")	"not_enough_gold"

#                         변수의 이름   테스트 케이스
@pytest.mark.parametrize("name,             body,                         status,      error_code", 
                        [("없는 아이템",  {"item_id":999 , "qauntity":1},        404,   "ITEM_NOT_FOUND" ),
                        ("수량 0",      {"item_id": 101, "quantity": 0},       422,   "INVALID_QUANTITY"),
                        ("수량 100",    {"item_id": 101, "quantity": 100},     422,   "INVALID_QUANTITY"),
                        ("골드 부족",    {"item_id": 103, "quantity": 99},      400,   "NOT_ENOUGH_GOLD")]  )

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