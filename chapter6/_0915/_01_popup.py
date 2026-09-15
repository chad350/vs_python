import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://302lab.co.kr/websample/selenium-demo/03_%EC%95%8C%EB%A6%BC%EC%B0%BD_%ED%8C%9D%EC%97%85")


el_btn_notice = driver.find_element(By.ID, "notice-btn")
el_btn_notice.click()

# 확인 버튼이 하나있는 confirm 
# accept 로 확인
alert = driver.switch_to.alert
alert_msg = alert.text # <- 미리 alert 정보를 체크
alert.accept()   # <- alert 종료
# print(alert.text)  <- alert 종료된 상태에서 접근은 X

el_btn_recall = driver.find_element(By.ID, "recall-btn")
el_btn_recall.click()

# 확인 버튼과 취소 버튼 2가지가 있는 경우
# 확인 - accecpt
# 취소 - dismiss 
alert = driver.switch_to.alert
alert.dismiss()


el_btn_slow_recall = driver.find_element(By.ID, "recall-slow-btn")
el_btn_slow_recall.click()

wait = WebDriverWait(driver, 10)

alert = wait.until(
    EC.alert_is_present(),
    "alert 이 뜨지 않았습니다,"  # 메시지를 남기는 선택 옵션
)

print(alert.text)
alert.accept()


# prompt - 메시지 입력창이 있는 팝업
# send_keys(msg) - 입력 가능
# accept / dismiss
el_btn_ban = driver.find_element(By.ID, "ban-btn")
el_btn_ban.click()

alert = driver.switch_to.alert
alert.send_keys("닉네임이 중복되어 있습니다.")
alert.accept()

# modal
# HTML 요소를 이용해서 팝업이나 추가 페이지를 만든 것
# find_element / click / send_keys 등 기존 element 조작과 동일하게 사용
el_btn_modal = driver.find_element(By.ID, "open-modal-btn")
el_btn_modal.click()

time.sleep(2)

el_btn_close = driver.find_element(By.ID, "modal-close-btn")
el_btn_close.click()


input()