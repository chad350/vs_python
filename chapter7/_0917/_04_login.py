import re
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

url = "https://302lab.co.kr/websample/selenium-advanced-demo/a05_admin_signup_signin"

try_url = url + "?view=dashboard"


driver.get(try_url)
driver.delete_all_cookies()

print("try :", try_url) # 처음 시도한 주소
print("current :", driver.current_url) # 현재 들어와진 주소

# url 포함 여부를 체크할 수 있다.
wait.until(
    EC.url_contains("view=login")
)

el_login_notice = driver.find_element(By.ID, "login-notice")
print(el_login_notice.text)

# 로그인 되었을떄 활성화
el_nav_avatar = driver.find_element(By.ID, "nav-avatar") 
el_btn_logout = driver.find_element(By.ID, "nav-logout-btn")

# 로그인 안되었을떄 활성화
el_nav_login = driver.find_element(By.ID, "nav-login-btn")
el_btn_login = driver.find_element(By.ID, "login-submit")

print("로그인 전")
print("el_nav_avatar :", el_nav_avatar.is_displayed())
print("el_btn_logout :", el_btn_logout.is_displayed())
print("el_nav_login :", el_nav_login.is_displayed())
print("el_btn_login :", el_btn_login.is_displayed())





el_input_email = driver.find_element(By.NAME, "login-email")
el_input_email.send_keys("luna@moon.gg")

el_input_pw = driver.find_element(By.NAME, "login-pw")
el_input_pw.send_keys("moonlight8")

el_login = driver.find_element(By.ID, "login-submit")
print(f"로그인 버튼 활성화 : {el_login.is_enabled()}")

wait.until(
    EC.element_to_be_clickable((By.ID, "login-submit"))
)

el_login.click()



wait.until(
    EC.url_contains("view=dashboard")
)


print("로그인 후")

# 로그인 되었을떄 활성화
el_nav_avatar = driver.find_element(By.ID, "nav-avatar") 
el_btn_logout = driver.find_element(By.ID, "nav-logout-btn")

# 로그인 안되었을떄 활성화
el_nav_login = driver.find_element(By.ID, "nav-login-btn")
el_btn_login = driver.find_element(By.ID, "login-submit")

print("el_nav_avatar :", el_nav_avatar.is_displayed())
print("el_btn_logout :", el_btn_logout.is_displayed())
print("el_nav_login :", el_nav_login.is_displayed())
print("el_btn_login :", el_btn_login.is_displayed())

input()