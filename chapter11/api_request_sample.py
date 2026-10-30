import requests

BASE_URL = "https://guild-expedition.fly.dev"


# API 요청 하는 방법
# - requests.get("url")
# - requests.post("url")


# get 요청
# response = requests.get(BASE_URL + "/status")

# 1. 후보 정보 요청
# response = requests.get(BASE_URL + "/heroes/candidates/30")

#  - get 요청시 param 적용하는 방법
# response = requests.get(BASE_URL + "/heroes/candidates", params= {  "job" : "전사" } )  # param 1개
# response = requests.get(BASE_URL + "/heroes/candidates", params=  {  "job" : "전사" , "sort" : "power" } ) # param 2개


# 2. 로그인 - Token  [post]
# - body 전달 - json 형식
response = requests.post(BASE_URL + "/auth/token", json= {  "username" : "elice_guild" , "password" : "elice_1234"} )
token = response.json()["access_token"]


# 3. 길드 정보 요청
# - 토큰 설정 규칙 - 앞에 Bearer 붙이기
#   Bearer 5c1f1288d0f84ce4b2706b92a152adf5
# - header 를 통해 전달
response = requests.get(BASE_URL + "/guild", headers= {  "Authorization" : "Bearer " + token  })

# 길드 리셋 - 테스트 초기화
response = requests.post(BASE_URL + "/guild/reset", headers= {  "Authorization" : "Bearer " + token  } )


# 4. 인증키 발급 
response = requests.get(BASE_URL + "/guild/api-key", headers= {  "Authorization" : "Bearer " + token  })
api_key = response.json()["api_key"]


# 5. 주간 보스 정보 (API 키 활용)
# API 키값 전달 - header 를 통해 전달
response = requests.get(BASE_URL + "/open/weekly-boss", headers= {  "X-API-Key" : api_key  })


# 6. 후보 확인
response = requests.get(BASE_URL + "/heroes/candidates", params= {  "limit" : 20  })

# - 응답 시간을 확인
print("elapsed :", response.elapsed.total_seconds())

# - 헤더에 있는 데이터를 읽는 방법
content_type = response.headers["Content-Type"]
print("content_type :", content_type)

# - 데이터의 크기 확인
print("데이터의 크기 :", len(response.content)) 

# - 성공 여부  / status_code 가 400 미만 경우
print("요청 성공 :", response.ok)


headers = {  "Authorization" : "Bearer " + token  }

response = requests.post(BASE_URL + "/guild/heroes", headers=headers,  json={  "candidate_id" : 1  })

response = requests.post(BASE_URL + "/guild/orders", headers=headers,  json={  "item_id": 102, "quantity": 1  })
response = requests.post(BASE_URL + "/guild/orders", headers=headers,  json={  "item_id": 201, "quantity": 1  })

# put 메서드 사용
# 전체 데이터 수정
response = requests.put(BASE_URL + f"/guild/heroes/{1}/equipment", headers=headers,  json={ "weapon": 102, "armor": 201 })

# patch 메서드 사용
# 일부 데이터 수정
response = requests.patch(BASE_URL + f"/guild/heroes/{1}", headers=headers,  json={ "name" : "빛의 아린" })


# delete 메서드 사용
response = requests.delete(BASE_URL + f"/guild/heroes/{1}", headers=headers)



print("status_code :", response.status_code)
# print("json : ",response.json())