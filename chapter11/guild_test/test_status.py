import requests
import pytest

BASE_URL = "https://guild-expedition.fly.dev" 

# 서버 상태를 체크하는 기능
@pytest.mark.smoke
def test_server_status():
    response = requests.get(f"{BASE_URL}/status")
    assert response.status_code == 200, f"[서버 상태] 기대 : 200 , 실제 {response.status_code}"

    status = response.json()["status"]
    assert status == "ok", f"[status] 기대 : ok ,  실제 : {status}"


# 후보 목록을 조회
@pytest.mark.smoke
def test_candidate_list():
    response = requests.get(f"{BASE_URL}/heroes/candidates")
    data = response.json()
    print("응답 본문 :", data)

    assert response.status_code == 200, f"[서버 상태] 기대 : 200 , 실제 {response.status_code}"
    assert data["total"] == 12, f"[전체 후보수] 기대 : 12 , 실제 {data["total"]}"
    assert len(data["items"]) == 5, f"[1페이지의 인원]  기대 : 5 ,  실제 : {len(data["items"])}"
    assert data["total_pages"] == 3, f"[전체 페이지]  기대 : 3 ,  실제 : {data["total_pages"]}"