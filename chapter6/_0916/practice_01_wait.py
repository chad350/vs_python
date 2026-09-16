import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

driver.get("https://302lab.co.kr/websample/selenium-control/p5_쿠폰등록")

wait = WebDriverWait(driver, 10)

# Q3
el_btn_apply = driver.find_element(By.ID, "apply-btn")
el_btn_apply.click()

# option 1
# wait.until(
#     EC.invisibility_of_element_located((By.ID, "apply-overlay"))
# )

# option 2
# wait.until(
#     EC.text_to_be_present_in_element((By.ID, "apply-msg"), "쿠폰 2장 적용 완료")
# )

el_msg_apply = driver.find_element(By.ID, "apply-msg")
print(el_msg_apply.text)


input()