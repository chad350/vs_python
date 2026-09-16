import time
import logging
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Chrome()


# 우리가 일반 크롬이나 실제로 쓰는 브라우저에서 사용할때
# 기존에 사용하던 로그인 정보나, 여러 사용데이터들이 이미 쿠키로 등록

# selenium 의 driver 통해서 접속하는 경우
# driver 로 연 페이지는 새로운 브라우저 -> 빈 쿠키에서 시작 

# 쿠팡에 접속하면서 여러 쿠키 세팅이 되어 몇개라도 보인것
# driver.get("https://www.coupang.com/")



start_url = driver.current_url
start_cookies = driver.get_cookies()  #  없다면 빈 list   [  ]

print("start_url :", start_url)
print("start_cookies :", start_cookies)

# 검증
assert start_cookies == [], "브라우저의 쿠키가 세팅되어 있습니다."


driver.get("https://302lab.co.kr/websample/selenium-advanced-demo/a01_admin_login_cookie")

el_input_apply = driver.find_element(By.ID, "apply-id")
el_input_apply.send_keys("new_helper")

el_btn_apply = driver.find_element(By.ID, "apply-btn")
el_btn_apply.click()

cookies = driver.get_cookies()
print(cookies) # [{'domain': '302lab.co.kr', 'expiry': 1792134895, 'httpOnly': False, 'name': 'adv01_op_theme', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'light'}]

for c in cookies:
    print(c["domain"])
    print(c["expiry"])
    print(c["name"])
    print(c["value"])


el_id_op = driver.find_element(By.ID, "op-id")
el_id_op.send_keys("moon_admin")

el_pw_op = driver.find_element(By.ID, "op-pw")
el_pw_op.send_keys("moon1234")

el_btn_keep = driver.find_element(By.ID, "keep-login")
el_btn_keep.click()


el_btn_login = driver.find_element(By.ID, "login-btn")
el_btn_login.click()



wait = WebDriverWait(driver, 10)

wait.until(
    EC.visibility_of_element_located((By.ID, "console-section"))
)

cookies = driver.get_cookies()

# expiry
# 있으면 영구 쿠키 - 브라우저 닫아도 유지됨
# 없으면 세션 쿠키 - 브라우저 닫으면 없어짐

token_cookie = {}

for c in cookies:
    expiry = c.get("expiry", 0)
    print(f"cookie data - name : {c['name']}   value : {c['value']}    expiry : {expiry} ")
    if c['name'] == "adv01_op_token":
        token_cookie = c


# keep 안했을때
# cookie data - name : adv01_op_token   value : OPTK-7A1C    expiry : 0 
# cookie data - name : adv01_op_theme   value : light    expiry : 1792135822 
# cookie data - name : adv01_op_name   value : moon_admin    expiry : 0 

# keep 했을때
# cookie data - name : adv01_op_name   value : moon_admin    expiry : 0 
# cookie data - name : adv01_op_theme   value : light    expiry : 1792136034 
# cookie data - name : adv01_op_token   value : OPTK-7A1C    expiry : 1790148835 

# 2026-09-23 4:41

# 토큰 기간
expiry = c.get("expiry", 0)

# 1970
dist =  expiry - time.time() 
print("만료시간 :", expiry)       # 1790149278   - 9월 23일 4:41
print("현재시간 :", time.time())  # 1789544478   - 9월 16일 4:41
print("차이 :", dist)

# 하루 - 86400초
# 1일 - 86400
# 2일 - 172,800
# 3일 - 259,200
# 7일 - 604,800
print(dist / 86400)  # 일자 단위로 체크
# 6.999993532860168 -> 7 



# driver.get_cookies() - 지금 쿠키 목록 전체를 가지고 올 수 있음
# driver.get_cookie("쿠키의 키값") - 지금 쿠키 목록중에 원하는 쿠키를 가지고 올 수 있음

token_cookie = driver.get_cookie("adv01_op_token")
print("login 을 위한 토큰 :", token_cookie)


el_btn_logout = driver.find_element(By.ID, "logout-btn")
el_btn_logout.click()
print("로그아웃!")


token_cookie = driver.get_cookie("adv01_op_token")
print("login 을 위한 토큰 :", token_cookie)











input()