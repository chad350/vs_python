import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("https://302lab.co.kr/websample/selenium-control/p1_상품상세")

# Q1.패키지의 이름과 가격
el_product_name = driver.find_element(By.ID, "product-name")
el_price = driver.find_element(By.ID, "price")

val_product_name = el_product_name.text

# 문자를 숫자로
# "₩ 33,000" -> 33000
str_price = el_price.text.replace("₩","")
str_price = str_price.replace(",","")
str_price = str_price.strip()
val_price = int(str_price)

# Q2.할인률과 정가
el_discount = driver.find_element(By.ID, "discount")
el_original_price = driver.find_element(By.ID, "original-price")

# 20% 할인 -> 20
val_discount = int(el_discount.text.replace("% 할인","").strip())
# ₩ 41,250 -> 41250
val_original_price = int(el_original_price.text.replace("₩","").replace(",","").strip())


# Q3.구매 제한과 입력칸 확인(현재값, 최댓값)
el_limit = driver.find_element(By.ID, "limit")
el_input_qty = driver.find_element(By.ID, "qty")

val_limit = int(el_limit.text)
val_qty_max = int(el_input_qty.get_attribute("max"))
val_qty_cur = int(el_input_qty.get_attribute("value"))

assert val_qty_max == val_limit, "최대 수량과 인풋 최대값이 맞지 않습니다."

# Q4.상품 안내링크를 원문그대로 출력
el_detail_link = driver.find_element(By.ID, "detail-link")
val_detail_link = el_detail_link.get_dom_attribute("href")

# Q5.품절문구가 보이는지 확인, 할인기간에 "9월 20일"이 포함되는지 확인
el_sold_out = driver.find_element(By.ID, "sold-out-note")
el_event_note = driver.find_element(By.ID, "event-note")

print(el_sold_out.is_displayed())
print("9월 20일" in el_event_note.text)

# Q6. 구매 버튼이 활성화가 되어 있는지 체크, 클릭
el_btn_buy = driver.find_element(By.ID, "buy-btn")
print(el_btn_buy.is_enabled())
el_btn_buy.click()

# Q7.체크박스와 라디오 버튼의 상태 확인, 동의하기 누르기, 구매버튼 상태 확인
el_agree_terms = driver.find_element(By.ID, "agree-terms")
el_agree_refund = driver.find_element(By.ID, "agree-refund")
el_pay_card = driver.find_element(By.ID, "pay-card")
el_pay_point = driver.find_element(By.ID, "pay-point")
el_pay_gift = driver.find_element(By.ID, "pay-gift")

print("체크박스 확인")
print("약관동의 :", el_agree_terms.is_selected())
print("환불동의 :", el_agree_refund.is_selected())

print("라디오 버튼 확인")
print("카드 구매 :", el_pay_card.is_selected())
print("포인트 구매 :", el_pay_point.is_selected())
print("선물 코드 구매 :", el_pay_gift.is_selected())

el_agree_terms.click()

print("구매 버튼 활성화 :",el_btn_buy.is_enabled())

# Q8.수량을 2로 바꾸고 구매 / 완료 문구과 재고 확인

# 수를 넣는게 아니라 문자를 입력
# send_keys <- 값을 바꾸는게 아니라 "추가!!" 하는 것
# 바꾸고 싶다면 clear 하고 나서 입력
el_input_qty.clear()
el_input_qty.send_keys("2")
el_btn_buy.click()

el_stock = driver.find_element(By.ID, "stock")
el_buy_msg = driver.find_element(By.ID, "buy-msg")

print(int(el_stock.text))
print(el_buy_msg.text)


# Q9.찜 수 확인, 찜 2번 클릭, 찜 수 다시 확인
el_wish_btn = driver.find_element(By.ID, "wish-btn")
el_wish_count = driver.find_element(By.ID, "wish-count")

print(el_wish_count.text)

el_wish_btn.click()
el_wish_btn.click()

print(el_wish_count.text)


input()

