import time
import re
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)


driver.get("https://302lab.co.kr/websample/selenium-advanced-demo/a03_shop_list_collect")

el_cards = driver.find_elements(By.CLASS_NAME, "item-card")
print(f"카드 개수 : {len(el_cards)} 개")

el_cards = wait.until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "item-card")),
    "대기 실패 메시지"
)

print(f"카드 개수 : {len(el_cards)} 개")



# 삼품 아이디   item-card
# 상품 이름   item-name
# 상품 가격 < - 정수   item-price
# 상품 이미지  thumb
# 상세보기 링크   detail-link


cards = []

# 2가지
# 1. class      <- 
# 2. dictionary <-


test = [1,2,3]

test_dict = {
    "first" : 1,
    "second" : 2,
    "third" : 3
}



for el in el_cards:

    el_thumnail = el.find_element(By.CLASS_NAME, "thumb")
    el_item_name = el.find_element(By.CLASS_NAME, 'item-name')
    el_item_price = el.find_element(By.CLASS_NAME, 'item-price')
    el_item_link = el.find_element(By.CLASS_NAME, 'detail-link')

    item_id = el.get_attribute("data-item-id")
    item_name = el_item_name.text
    item_link = el_item_link.get_attribute("href")
    item_lmage = el_thumnail.get_attribute("src")

    price = re.sub( r"[^0-9]" , "" , el_item_price.text)
    item_price = int(price)

    card_dict = {
        "id" : item_id,
        "name" : item_name,
        "price" : item_price,
        "link" : item_link,
        "img" : item_lmage
    }

    cards.append(card_dict)
    # print(f"[{item_id}] 아이템 이름 : {item_name}  가격 :  {item_price},     img : {item_lmage}   link : {item_link}")



for card in cards :
    print(card["name"])

total = 0
for card in cards :
    total+= card["price"]    

print(total)


# 각격만 모아진 배열
price_list = [card["price"] for card in cards]
print(sum(price_list))

# print(sum([card["price"] for card in cards]))


input()