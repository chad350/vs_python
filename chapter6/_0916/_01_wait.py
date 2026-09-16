import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

driver.get("https://302lab.co.kr/websample/selenium-demo/05_%EB%8F%99%EA%B8%B0%ED%99%94")

wait = WebDriverWait(driver, 10)

el_btn_load = driver.find_element(By.ID, "load-btn")
el_btn_load.click()

el_table_rank = driver.find_element(By.ID, "rank-table")
print("데이터 로드 확인 :", el_table_rank.is_displayed())

el_table_rank = wait.until(
    EC.visibility_of_element_located((By.ID, "rank-table")),
    "에러 메시지"
)
print("데이터 로드 확인 :", el_table_rank.is_displayed())

el_btn_export = wait.until(
    EC.element_to_be_clickable((By.ID, "export-btn")),
    "에러 메시지"
)

el_btn_export.click()

el_btn_save = driver.find_element(By.ID, "save-btn")
el_btn_save.click()

wait.until(
    EC.invisibility_of_element_located((By.ID, "loading-overlay"))
)

el_msg = driver.find_element(By.ID, "save-msg")
print("완료 메시지 :", el_msg.text)



input()