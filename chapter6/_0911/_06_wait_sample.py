import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)


driver.get("https://302lab.co.kr/websample/selenium-demo/05_%EB%8F%99%EA%B8%B0%ED%99%94")

el_btn_load = driver.find_element(By.ID, "load-btn")
el_btn_load.click()

el_rank = wait.until(
    EC.visibility_of_element_located((By.ID, "rank-area")),
    "대상이 렌더링 되지 못했습니다."
)

el_trs = el_rank.find_elements(By.TAG_NAME, "tr")

for tr in el_trs:
    print(tr.text)

input()