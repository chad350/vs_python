import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("https://302lab.co.kr/websample/selenium-demo/01_%EA%B0%92%EC%9D%BD%EA%B8%B0_%EA%B2%80%EC%A6%9D")


# id - nickname 
# nick-name 이라고 검색헀을때 원하는 요소를 찾을 수 없을떄 나타나는 에러
# -> NoSuchElementException
# 오타 잘못 검색을 했을떄
# el_id = driver.find_element(By.ID, "nick-name")

# 숨어있는 버튼
# 상호작용이 불가능한 상태
#  -> ElementNotInteractableException
# is_displayed
# el_btn_hidden = driver.find_element(By.ID, "hidden-btn")
# el_btn_hidden.click()

# readonly 를 clear 하려고 할떄
# -> InvalidElementStateException
# el_input_date = driver.find_element(By.ID, "joined")
# el_input_date.clear()


input()