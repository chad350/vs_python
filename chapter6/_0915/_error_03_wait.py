import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://302lab.co.kr/websample/selenium-demo/05_%EB%8F%99%EA%B8%B0%ED%99%94")

wait = WebDriverWait(driver, 1)

# 지정한 시간 동안 찾기 못하면
#  -> TimeoutException : 기본적으로는 추가적인 메시지가 없음
#  until 의 두번째 매개변수로 메시지 입력가능
wait.until(
    EC.visibility_of_element_located((By.ID, "test")),
    "시간이 될 때까지 찾지 못했습니다."
)







input()