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

driver.get("https://302lab.co.kr/websample/selenium-advanced/s03_product_list_collect")


el_goods = driver.find_elements(By.CLASS_NAME, "goods-row")
first_search_count = len(el_goods)
print("처음 실행 후 아이템 수 : ", first_search_count)

el_goods = wait.until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "goods-row"))
)

print("로딩 후 아이템의 수", len(el_goods))

goods = []

for el in el_goods:
    el_name = el.find_element(By.CLASS_NAME, "g-name")
    el_price = el.find_element(By.CLASS_NAME, "g-price")
    el_link = el.find_element(By.CLASS_NAME, "g-link")

    goods_name = el_name.text

    price = re.sub( r"[^0-9]" , "" , el_price.text)
    goods_price = int(price)  # ₩33,000 

    # bool         "자세히"    == "판매 준비 중" 
    goods_link = el_link.text == "자세히"

    goods.append( {
        "name" : goods_name, 
        "price" : goods_price, 
        "sell" : goods_link
    } )


# 판매 중인 상품 수
sell_goods = [i for i in goods if i["sell"]]
print("판매중 아이템 수 :", len(sell_goods))

# 고가 상품
rare_goods = [i for i in goods if i["price"] >= 10000]

# 고가 상품 이름 목록
rare_goods_name = [i["name"] for i in rare_goods]
print("고가 상품 이름 :", rare_goods_name)

# 고가 상품 가격 합계
rare_goods_sum = sum([i["price"] for i in rare_goods])
print("고가 상품 가격 합계 :", rare_goods_sum)


# 판매 중 가장 싼 상품 이름
min_price = 9999999
min_name = ""
for item in sell_goods:
    if item["price"] <= min_price:
        min_price = item["price"]
        min_name = item["name"]

print("가장 저렴한 상품 :", min_name)


assert first_search_count == 0, f"처음 실행 후 아이템 수가  0이 아닙니다.  실제 값 : {first_search_count}"
assert len(el_goods) == 8, f"로딩 후 아이템의 수가 8이 아닙니다.    실제 값 : {len(el_goods)}"
assert len(sell_goods) == 7, f"판매중 아이템 수가 7이 아닙니다    실제 값 : {len(sell_goods)}"
assert rare_goods_name == ['달빛 망토', '여행자 가방', '길드 깃발', '소환권 10장'], f"고가 아이템 리스트가 맞지 않습니다.   실제 값 : {rare_goods_name}"
assert rare_goods_sum == 90900, f"고가 상품 가격 합계가 90900 이 아닙니다.   실제 값 : {rare_goods_sum}"
assert min_name == "은하 물약 세트", f"가장 저렴한 상품이 은하 물약 세트가 아닙니다.    실제 값 : {min_name}"


print("테스트 완료")




input()