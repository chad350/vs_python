import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

driver = webdriver.Chrome()
driver.get("https://302lab.co.kr/websample/selenium-demo/02_%EB%93%9C%EB%A1%AD%EB%8B%A4%EC%9A%B4")

el_btn_rarity = driver.find_element(By.ID, "rarity-btn")
el_btn_rarity.click()

time.sleep(2)

el_option_r = driver.find_element(By.CSS_SELECTOR, "[data-value='r']")
el_option_r.click()



# ["아르티아", "아르곤", "아르카나", "루아", "루시엘", "미르"];
target_user = "아르카나"
search_keyword = "아르"

el_input_player = driver.find_element(By.ID, "player-input")
el_input_player.send_keys(search_keyword)
el_input_player.send_keys(Keys.ENTER)
time.sleep(1)

# el_option_players = driver.find_elements(By.CSS_SELECTOR, "#player-list .player-item")
el_option_players = driver.find_elements(By.CLASS_NAME, "player-item")

time.sleep(1)

result = False


for player in el_option_players:
    if player.text == target_user :
        player.click()
        result = True

assert result,f"유저를 찾지 못했습니다. : {target_user}"

input()

