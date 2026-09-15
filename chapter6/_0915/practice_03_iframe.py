import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://302lab.co.kr/websample/selenium-control/p4_결제창")

# Q3
el_frame_policy = driver.find_element(By.ID, "policy-frame")
driver.switch_to.frame(el_frame_policy)

el_policy_version = driver.find_element(By.ID, "policy-version")
el_policy_agree = driver.find_element(By.ID, "policy-agree")

print(el_policy_version.text)
if not el_policy_agree.is_selected():
    el_policy_agree.click()


# Q4
driver.switch_to.default_content()
el_email = driver.find_element(By.ID, "receipt-email")
print(el_email.get_attribute("value"))


input()