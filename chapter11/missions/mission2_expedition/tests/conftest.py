import pytest
import requests

BASE_URL = "https://guild-expedition.fly.dev"
USERNAME = "student01"   # 내 아이디로 바꿉니다
PASSWORD = "guild1234"


@pytest.fixture(scope="session")
def token():
    print("\n로그인 실행")
    response = requests.post(BASE_URL + "/auth/token", json={"username": USERNAME, "password": PASSWORD})
    return response.json()["access_token"]


@pytest.fixture
def guild(token):
    headers = {"Authorization": "Bearer " + token}
    requests.post(BASE_URL + "/guild/reset", headers=headers)
    print("초기화 · 테스트 전")
    yield headers
    requests.post(BASE_URL + "/guild/reset", headers=headers)
    print("\n초기화 · 테스트 뒤")
