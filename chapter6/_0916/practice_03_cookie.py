import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

driver.get("https://302lab.co.kr/websample/selenium-advanced/s01_account_center_cookie")

wait = WebDriverWait(driver, 10)


# Q1. 회원가입 직후 쿠키 목록 확인
el_join_nick = driver.find_element(By.ID, "join-nick")
el_join_nick.send_keys("luna77")

el_join_email = driver.find_element(By.ID, "join-email")
el_join_email.send_keys("luna@moon.shop")

el_join_pw = driver.find_element(By.ID, "join-pw")
el_join_pw.send_keys("star2026")

el_join_btn = driver.find_element(By.ID, "join-btn")
el_join_btn.click()

wait.until(
    EC.text_to_be_present_in_element((By.ID, "join-result"), "가입 완료"),
    "가입 완료 메시지가 나오지 않았습니다."
)

cookies = driver.get_cookies()
print(cookies)


# Q2. 로그인 쿠키를 이름으로 읽기
el_signin_email = driver.find_element(By.ID, "signin-email")
el_signin_email.send_keys("luna@moon.shop")

el_signin_pw = driver.find_element(By.ID, "signin-pw")
el_signin_pw.send_keys("star2026")

el_signin_btn = driver.find_element(By.ID, "signin-btn")
el_signin_btn.click()

wait.until(
    EC.visibility_of_element_located((By.ID, "mypage-box"))
)


print("adv01_shop_sid : ", driver.get_cookie("adv01_shop_sid"))
print("adv01_shop_nick : ", driver.get_cookie("adv01_shop_nick"))



# Q3. 로그아웃과 로그인 유지 기간 계산
el_signout_btn = driver.find_element(By.ID, "signout-btn")
el_signout_btn.click()

print("adv01_shop_sid : ", driver.get_cookie("adv01_shop_sid"))


el_remember = driver.find_element(By.ID, "remember-me")
el_remember.click()

el_signin_btn = driver.find_element(By.ID, "signin-btn")
el_signin_btn.click()

wait.until(
    EC.visibility_of_element_located((By.ID, "mypage-box"))
)


login_cookie = driver.get_cookie("adv01_shop_sid")

expire_time = login_cookie["expiry"]
currenrt_time = time.time()

# 얼마나 남았는지 - 초로 표현
dist = expire_time - currenrt_time

# 얼마나 남았는지 - 일자로 계산
remain_day = dist / 86400

print(remain_day)

assert 29 < remain_day < 30, "로그인 유지시간이 30일이 되지 않았습니다."

input()