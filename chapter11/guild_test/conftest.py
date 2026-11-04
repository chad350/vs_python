import requests
import pytest

BASE_URL = "https://guild-expedition.fly.dev" 
USERNAME = "elice_chad"
PASSWORD = "elice_1234"



# 픽스처 샘플
@pytest.fixture(scope="session")
def token():
    response = requests.post(f"{BASE_URL}/auth/token", json={ "username":USERNAME , "password":PASSWORD })
    return response.json()["access_token"]


@pytest.fixture
def guild_auth(token):
    h = { "Authorization" : f"Bearer {token}"}
    
    requests.post(f"{BASE_URL}/guild/reset" , headers=h)
    print("\n초기화 - 테스트 전")
    
    yield h

    requests.post(f"{BASE_URL}/guild/reset" , headers=h)
    print("\n초기화 - 테스트 전")






