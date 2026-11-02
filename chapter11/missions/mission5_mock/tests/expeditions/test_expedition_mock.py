import time

import pytest
import requests
import responses

BASE_URL = "https://guild-expedition.fly.dev"
URL = BASE_URL + "/guild/expeditions/1"


def wait_until_completed(headers, expedition_id, max_try=15, interval=1):
    for poll_count in range(1, max_try + 1):
        time.sleep(interval)
        response = requests.get(BASE_URL + f"/guild/expeditions/{expedition_id}", headers=headers)
        if response.json()["status"] == "COMPLETED":
            return poll_count
    return None


@responses.activate
def test_wait_returns_poll_count():
    responses.add(responses.GET, URL, json={"expedition_id": 1, "status": "IN_PROGRESS"}, status=200)
    responses.add(responses.GET, URL, json={"expedition_id": 1, "status": "IN_PROGRESS"}, status=200)
    responses.add(responses.GET, URL, json={"expedition_id": 1, "status": "COMPLETED"}, status=200)

    poll_count = wait_until_completed({}, 1, max_try=5, interval=0)
    assert poll_count == 3, f"조회 횟수: 기대 3, 실제 {poll_count}"
    assert len(responses.calls) == 3, f"요청 횟수: 기대 3, 실제 {len(responses.calls)}"


@responses.activate
def test_wait_gives_up():
    # TODO 1 · URL 에 IN_PROGRESS 응답 1개를 등록합니다 (마지막 응답은 계속 반환됩니다)
    pytest.skip("TODO 1 작성 전 · 작성하면 이 행을 지웁니다")
