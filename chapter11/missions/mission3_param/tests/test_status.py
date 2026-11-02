import requests

BASE_URL = "https://guild-expedition.fly.dev"


def test_server_status():
    response = requests.get(BASE_URL + "/status")
    assert response.status_code == 200, f"서버 상태: 기대 200, 실제 {response.status_code}"

    data = response.json()
    assert data["status"] == "ok", f"status: 기대 ok, 실제 {data['status']}"


def test_candidate_list():
    response = requests.get(BASE_URL + "/heroes/candidates")
    data = response.json()
    print("응답 본문:", data)

    assert response.status_code == 200, f"후보 목록: 기대 200, 실제 {response.status_code}"
    assert data["total"] == 12, f"전체 후보 수: 기대 12, 실제 {data['total']}"
    assert len(data["items"]) == 5, f"1페이지 인원: 기대 5, 실제 {len(data['items'])}"
    assert data["total_pages"] == 3, f"전체 페이지: 기대 3, 실제 {data['total_pages']}"


def test_candidate_not_found():
    response = requests.get(BASE_URL + "/heroes/candidates/99")
    assert response.status_code == 404, f"없는 후보: 기대 404, 실제 {response.status_code}"
    assert response.json()["error_code"] == "CANDIDATE_NOT_FOUND"
