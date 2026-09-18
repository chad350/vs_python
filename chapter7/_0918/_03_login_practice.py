import time
import re
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = "https://302lab.co.kr/websample/game-site"

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 5)

print("\n=== 1단계. 오류 문구는 나타날 때까지 기다린 뒤 읽어야 합니다 ===")

driver.get(url + "/login.html?reset=1")

el_login_name = driver.find_element(By.ID, "login-email")
el_login_name.send_keys("artia@moon.gg")

el_login_pw = driver.find_element(By.ID, "login-pw")
el_login_pw.send_keys("0000")

el_btn_login = wait.until(
    EC.element_to_be_clickable((By.ID, "login-btn"))
)

el_btn_login.click()


# 에러 메시지 저장
error_msg = driver.find_element(By.ID, "login-error").text
print(error_msg)

wait.until(
    EC.text_to_be_present_in_element((By.ID, "login-error"), "올바르지 않습니다")
)

wait_error_msg = driver.find_element(By.ID, "login-error").text

print("wait 전의 에러 메시지 : ", error_msg)
print("wait 후의 에러 메시지 : ", wait_error_msg)



print("\n=== 2단계. 로그인 상태는 쿠키 mg_session 에 저장됩니다 ===")

el_login_pw.clear()
el_login_pw.send_keys("artia2026")

el_btn_login.click()


# 로그인 완료를 기다린 것
wait.until(
    EC.visibility_of_element_located((By.ID, "nav-nick"))
)

# 쿠키 값을 통해서 로그인이 되었는지 검증
print("쿠킴 목록 확인 : ",driver.get_cookies())



login_cookie = driver.get_cookie("mg_session")
print("로그인 쿠키 : ",login_cookie)

cookie_name = login_cookie["value"]

assert cookie_name.startswith("MG-")

print("로그인 검증이 완료되었습니다.")


print("\n=== 3단계. 쿠키를 지우면 로그인이 풀리고, 보관한 쿠키를 넣으면 로그인 상태가 돌아옵니다 ===")

# 쿠키 값이 없을때 어떻게 로그인이 풀리는 것을 확인
driver.delete_cookie("mg_session")
driver.get(url + "/shop.html")

wait.until(
    EC.url_contains("/login")
)

print("쿠키 삭제 후")
print(f"시도한 주소 : {url + "/shop.html"}")
print(f"실제 도착 주소 : {driver.current_url}")


# 임의로 쿠키값을 다시 넣으줌
# 쿠키로 사용할 딕셔너리는 2가지 키
# name , value
driver.add_cookie( {  "name" : "mg_session",  "value" : cookie_name  } )

# 로그인 쿠키가 있는 상태로 기능을 활용하려고 함
driver.get(url + "/shop.html")

print("쿠키 적용 후")
print(f"시도한 주소 : {url + "/shop.html"}")
print(f"실제 도착 주소 : {driver.current_url}")




input()