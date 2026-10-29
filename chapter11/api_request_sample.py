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


# 4. 인증키 발급 
response = requests.get(BASE_URL + "/guild/api-key", headers= {  "Authorization" : "Bearer " + token  })
api_key = response.json()["api_key"]


# 5. 주간 보스 정보 (API 키 활용)
# API 키값 전달 - header 를 통해 전달
response = requests.get(BASE_URL + "/open/weekly-boss", headers= {  "X-API-Key" : api_key  })


print("status_code :", response.status_code)
print("json : ",response.json())