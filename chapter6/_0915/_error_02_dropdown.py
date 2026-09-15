import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

driver = webdriver.Chrome()
driver.get("https://302lab.co.kr/websample/selenium-demo/02_%EB%93%9C%EB%A1%AD%EB%8B%A4%EC%9A%B4")


# select tag 로 만들어 지지 않은 경우 Select() 로 감싸려고 하면 에러
#  -> UnexpectedTagNameException
# el_dropdonw_rarity = driver.find_element(By.ID, "rarity-btn")
# dropdown_rarity = Select(el_dropdonw_rarity)

# select tag 로 만들어진것은 전용 기능을 추가해서 감싸는 게 Select()
el_dropdonw_server = driver.find_element(By.ID, "server")
dropdown_server = Select(el_dropdonw_server)

# 없는 값으로 선택하려고 할때
#  -> NoSuchElementException
# dropdown_server.select_by_visible_text("미국 서버")

# 단일 선택 select -> deselect 
#  -> NotImplementedError
# dropdown_server.deselect_all()

# 항목의 요소가 활성화 되기 전에 조작하려고 했을때
#  -> ElementNotInteractableException
# el_btn_rarity = driver.find_element(By.ID, "rarity-btn")
# el_btn_rarity.click()
# ---- 대기가 필요 ----
# el_option_r = driver.find_element(By.CSS_SELECTOR, "[data-value='r']")
# el_option_r.click()


input()