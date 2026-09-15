import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

driver.get("https://302lab.co.kr/websample/selenium-control/p5_쿠폰등록")

el_input_code = driver.find_element(By.ID, "coupon-code")
el_btn_register = driver.find_element(By.ID, "register-btn")

el_input_code.send_keys("WRONG-1 ")
el_btn_register.click()

wait.until(
    EC.text_to_be_present_in_element((By.ID, "register-msg"), "존재하지 않는")
)

el_msg = driver.find_element(By.ID, "register-msg")

print(el_msg.text)






input()