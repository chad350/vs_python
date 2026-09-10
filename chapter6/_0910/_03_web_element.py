import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("https://302lab.co.kr/websample/css-selector/")

# element 
# - control ★★★
#   click, send_key, clear, submit(★)

# - get ★★★
#   text, tag_name, get_attribute(), get_propety()

# - check ★★★
#   is_displayed(), is_enabled(), is_selected() 

# - ect ★★
#   Select (드랍다운), switch_to (팝업), execute_script (js 스크립트 코드 실행)


time.sleep(2)

# 엘리멘트 찾아야 - find
input_id = driver.find_element(By.NAME, "email")
input_pw = driver.find_element(By.NAME, "password")
btn_login = driver.find_element(By.ID, "btn_login_7a3f")

# 조작 - control
input_id.send_keys("yyc2999@gmail.com")
input_pw.send_keys("123456789")

time.sleep(1)

btn_login.click()

input_search = driver.find_element(By.NAME, "keyword")
input_search.send_keys("키보드")
input_search.send_keys(Keys.ENTER)

time.sleep(2)

input_id.clear()
input_pw.clear()
input_search.clear()


input()