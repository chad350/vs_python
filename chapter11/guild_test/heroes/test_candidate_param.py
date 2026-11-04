import requests
import pytest

BASE_URL = "https://guild-expedition.fly.dev"


@pytest.mark.parametrize( "candidate_id, name" ,  [ (1, "아린") , 
                                                    (3, "카이") , 
                                                    (5, "세라"),
                                                    (7, "도윤") ]   )
def test_canditate_check_name(candidate_id, name):
    response = requests.get(f"{BASE_URL}/heroes/candidates/{candidate_id}")
    assert response.json()["name"] == name