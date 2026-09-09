import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


driver = webdriver.Chrome()
driver.get("https://www.naver.com/")

time.sleep(3)

# By.ID
# By.CLASS_NAME
# By.NAME

# By.CSS_SELECTOR
# By.XPATH
search_box = driver.find_element(By.ID, "query")

search_box.send_keys("엘리스")
search_box.send_keys(Keys.ENTER)

search_box.click()

input()