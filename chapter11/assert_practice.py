import requests

BASE_URL = "https://guild-expedition.fly.dev" 


# 3번 후보를 조회
response = requests.get(f"{BASE_URL}/heroes/candidates/3")
data = response.json()

# 1. 상태 코드를 검증
assert response.status_code == 200, f"[상태 코드] 기대 결과 : 200, 실제 : {response.status_code}"

# 2. 헤더를 체크
#   - 헤더의 원하는 데이터가 포함이 되어 있나?? (토큰값이 들어있는가?, 콘텐츠 타입이 들어있는가??)
#     있는지만 확인을 하는 기능
assert "Content-Type" in response.headers, "Content-Type 이 헤더에 없습니다."

#   - 헤더의 특정 필드의 값이 내가 원하는 값과 맞는지 
#     Content-Type 이 Json 인지, 인증 절차 Bearer token 인지
#     원하는 값이 들어가 있는지를 확인
assert response.headers["Content-Type"] == "application/json", f"Content-Type 이 application/json 아닙니다. 실제 : {response.headers['Content-Type']}"

# 3. 응답 시단
seconds = response.elapsed.total_seconds()
assert seconds < 1.0, f"[응답 시간 초과] 기대 결과 : 1초 미만,  실제 결과 : {seconds}"

# 4. 응단 본문의 타입
assert isinstance(data, dict), f"[본문 타입 매칭] 기대 결과 : dict,   실제 결과 : {type(data)}"

# 5. 본문의 내용 검증 
#  - json body 에 power 라는 값이 포함되어 있었는지
assert "power" in data, "power 값이 응답에 없습니다."

#  - json body 에 있는 name 의 값이 원하는 값이 맞는지
assert data["name"] == "카이", f"[본문 데이터 name] 기대 결과 : 카이 , 실제 결과 : {data["name"]}"


# 6. 후모의 목록 조회
response = requests.get(f"{BASE_URL}/heroes/candidates")
candidates = response.json()["items"]
assert len(candidates) > 0, "후보가 없습니다."
