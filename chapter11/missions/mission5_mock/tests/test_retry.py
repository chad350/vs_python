import time

import pytest
import requests
import responses

BASE_URL = "https://guild-expedition.fly.dev"


def get_with_retry(url, headers=None, max_try=3, interval=1):
    for attempt in range(1, max_try + 1):
        response = requests.get(url, headers=headers)
        if response.status_code != 500:
            return response
        if attempt < max_try:
            time.sleep(interval)
    return response


@responses.activate
def test_retry_succeeds_on_third_call():
    url = BASE_URL + "/guild/expeditions/1"
    # TODO 2 · url 에 500 → 500 → 200 순서로 응답 3개를 등록합니다
    pytest.skip("TODO 2 작성 전 · 작성하면 이 행을 지웁니다")


@responses.activate
def test_retry_gives_up_after_max_try():
    url = BASE_URL + "/guild/expeditions/1"
    # TODO 3 · url 에 500 응답을 3개 등록합니다 (for 문 또는 3행)
    pytest.skip("TODO 3 작성 전 · 작성하면 이 행을 지웁니다")


def test_real_server_needs_no_retry():
    response = get_with_retry(BASE_URL + "/status", max_try=3, interval=0)
    assert response.status_code == 200, f"서버 상태: 기대 200, 실제 {response.status_code}"
