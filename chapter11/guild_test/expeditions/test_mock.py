import requests
import responses

BASE_URL = "https://guild-expedition.fly.dev" 


# 이 테스트는 리스폰스틑 적용할 것이다 <- 체크
@responses.activate
def test_reward():

    # responses 를 이용해서 request 값을 미리 준비 ===========

    #                       요청 대상                                       |                  응답할 데이터
    #               요청할 메서드   ,           url                         ,            json          ,  status_code
    responses.add(responses.GET, f"{BASE_URL}/guild/expeditions/1"          , json={ "status" : "IN_PROGRESS" } , status = 400  )
    responses.add(responses.GET, f"{BASE_URL}/guild/expeditions/1"          , json={ "status" : "COMPLETED" } , status = 202  )
    responses.add(responses.POST, f"{BASE_URL}/guild/expeditions/1/reward"  , json={ "gold_reward" : 300 } , status = 202  )


    # request 를 통한 테스트 ==============================

    # 원정 정보를 조회
    # 1번째 요청
    result = requests.get(f"{BASE_URL}/guild/expeditions/1")
    print("\n[원정 상태 1] :", result.status_code)
    print("\n[결과값 1] :", result.json())

    # 2번째 요청
    result = requests.get(f"{BASE_URL}/guild/expeditions/1")
    print("\n[원정 상태 2] :", result.status_code)
    print("\n[결과값 2] :", result.json())
    assert result.json()["status"] == "COMPLETED"
    
    
    # 원정 보상을 획득
    result = requests.post(f"{BASE_URL}/guild/expeditions/1/reward")
    print("\n[보상 획득] :", result.status_code)
    print("\n[결과값] :", result.json())
    assert result.json()["gold_reward"] == 300


    # responses.calls <- 테스트한 요청에 기록
    print("\n[테스트 요청 횟수]", len(responses.calls))
    for call in responses.calls:
        print("[method]", call.request.method)
        print("[url]", call.request.url)