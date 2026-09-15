import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

driver = webdriver.Chrome()
driver.get("https://302lab.co.kr/websample/selenium-control/p2_결제")


# Q4. 
#  - 결제 수단 버튼 누르기
#  - 휴대폰 결제 선택
el_btn_method = driver.find_element(By.ID, "method-btn")
el_option_phone = driver.find_element(By.CSS_SELECTOR, "[data-value='phone']")

el_btn_method.click()
time.sleep(1)
el_option_phone.click()


# Q5. 
#  - 쿠폰 칸에 「축제」 를 입력
#  - 표시되는 목록에서 「축제 무료 배송」
#  - 목록에 없으면 실패로 처리한다.
el_input_coupon = driver.find_element(By.ID, "coupon-input")
el_input_coupon.send_keys("축제")
time.sleep(2)

el_items_coupon = driver.find_elements(By.CLASS_NAME, "coupon-item")
result = False
for item in el_items_coupon:
    if item.text == "축제 무료 배송":
        item.click()
        result = True

assert result, "축제 무료 배송 아이템이 없습니다."


# Q6
#  - 결제하기 버튼 누르기
#  - 결과 문구 확인 - print
el_btn_pay = driver.find_element(By.ID, "pay-btn")
el_btn_pay.click()

el_msg_pay = driver.find_element(By.ID, "pay-msg")
print(el_msg_pay.text)

msg_result = el_msg_pay.text

# "결제 완료: 초보자 패키지 (₩5,500) x1 / 신용카드"
# msg_result = "결제 실패: 초보자 패키지 (₩5,500) x1 / 신용카드"
# msg_result.split(':')[0]

result = msg_result[:5] == "결제 완료"

if result : 
    print("구매에 성공했습니다.")
else : 
    print("구매에 실패했습니다..")



input()