import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://302lab.co.kr/websample/selenium-demo/04_%EC%97%AC%EB%9F%AC%EC%B0%BD")

root_handle = driver.current_window_handle


# driver.switch_to.alert  # 1개 <- 바로 사용
# driver.switch_to.window()  # 여러개 <- 대상 지정 : handle
# driver.switch_to.frame()   # 여러개 <- 대상 지정 : 특별한 개념이 필요 X - iframe element O 

# 1. iframe element 찾아서
# 2. driver.switch_to.frame 로 전환
el_mail_frame = driver.find_element(By.ID, "mail-frame")
driver.switch_to.frame(el_mail_frame)

# iframe 요소 사용 - 기존과 동일
el_mail_title = driver.find_element(By.ID, "mail-title")
el_mail_title.clear()
el_mail_title.send_keys("iframe 창입니다!!!! 점검 보상입니다.")
print(el_mail_title.get_attribute("value"))

# iframe 에서 드라이버를 원래 페이지로 포커스 돌리는 방법
driver.switch_to.default_content()

# 원래 페이지로 전환 한 다음에 요소를 사용
el_preview = driver.find_element(By.ID, "preview")


input()