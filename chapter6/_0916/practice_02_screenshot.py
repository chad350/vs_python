import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

driver.get("https://302lab.co.kr/websample/selenium-control/p8_이벤트페이지")


path = "save_data/practice_02_screenshot"

Path(path).mkdir(parents=True, exist_ok=True)

# Q1. 요소만 촬용
el_banner_hero = driver.find_element(By.ID, "hero-banner")
el_banner_hero.screenshot(f"{path}/banner.png")


# Q4. 전체 촬영
el_footer = driver.find_element(By.ID, "foot")
driver.execute_script("arguments[0].scrollIntoView({block:'center'})", el_footer)
driver.save_screenshot(f"{path}/foot.png")



input()