import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://302lab.co.kr/websample/selenium-demo/03_%EC%95%8C%EB%A6%BC%EC%B0%BD_%ED%8C%9D%EC%97%85")


# 팝업이 뜨고 나서 alert 을 체크하고 accept
# alert 뜨지 않은 상태에서 접근
#  -> NoAlertPresentException
# driver.switch_to.alert



# alert 이 떠 있는 상태에서 웹을 조작을 하려고 함
# alert - accept / dismiss 완료 후에 다시 조작
#   -> UnexpectedAlertPresentException
# el_btn_notice = driver.find_element(By.ID, "notice-btn")
# el_btn_notice.click()
# el_recall = driver.find_element(By.ID, "recall")



# alert 창에 prompt 가 아닌경우(입력 메시지 칸이 없는 경우) send_keys 하려고하면 에러
#   -> ElementNotInteractableException
# el_btn_notice = driver.find_element(By.ID, "notice-btn")
# el_btn_notice.click()
# alert = driver.switch_to.alert
# alert.send_keys("test")



# 모달이 떠있는 상태에서 뒤에있는 버튼을 누르려고 할떄
#  -> ElementClickInterceptedException
# el_btn_modal = driver.find_element(By.ID, "open-modal-btn")
# el_btn_modal.click()

# el_btn_btn = driver.find_element(By.ID, "behind-btn")
# el_btn_btn.click()



input()