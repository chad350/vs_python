import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

driver = webdriver.Chrome()
driver.get("https://302lab.co.kr/websample/selenium-control/p2_결제")

el_product = driver.find_element(By.ID, "product")
dropdown_product = Select(el_product)

el_qty = driver.find_element(By.ID, "qty")
dropdown_qty = Select(el_qty)

el_gifts = driver.find_element(By.ID, "gifts")
dropdown_gifts = Select(el_gifts)




# Q1. 상품 드롭다운의 전체 항목 체크
for option in dropdown_product.options:
    print(option.text)

# Q2. 옵션 선택
# 상품 -> value pkg-festival
# 수량 -> 눈에 보이는 텍스트  3
dropdown_product.select_by_value("pkg-festival")
dropdown_qty.select_by_visible_text("3")

print("선택된 패키지 :",dropdown_product.first_selected_option.text)

# 사은품에서 프로필 테두리와 칭호를 고른다.
# 프로필 테두리를 해제한다.
# 남은 선택 항목을 확인한다.

dropdown_gifts.select_by_index(0)
dropdown_gifts.select_by_index(2)

time.sleep(1)

dropdown_gifts.deselect_by_value("frame")

time.sleep(1)

for option in dropdown_gifts.all_selected_options:
    print(option.text, "가 선택되어 있습니다.")

input()

