import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("https://302lab.co.kr/websample/selenium/02-search/")

# 찾아야 하는 요소 - 2가지
input_search = driver.find_element(By.ID, "searchBox") # 검색 창
btn_search = driver.find_element(By.ID, "searchButton") # 검색 버튼

input_search.send_keys("키보드")
btn_search.click()
time.sleep(1)

input_search.clear()

time.sleep(1)

input_search.send_keys("마우스")
btn_search.click()
time.sleep(1)

input_search.clear()

time.sleep(1)

input_search.send_keys("거치대")
btn_search.click()

time.sleep(1)

input_search.clear()

input()


# 키보드, 마우스, 거치대 <- 검색 가능한 내용