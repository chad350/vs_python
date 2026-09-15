import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://302lab.co.kr/websample/selenium-control/p3_장바구니")

# Q1
el_btn_cookie_accept = driver.find_element(By.ID, "cookie-accept-btn")
el_btn_checkout = driver.find_element(By.ID, "checkout-btn")

assert el_btn_cookie_accept.is_enabled()
assert el_btn_checkout.is_enabled()

# 다른 화면이 앞에 있어서 버튼을 누를 수 없는 상태
#  -> ElementClickInterceptedException
# el_btn_checkout.click()

el_btn_cookie_accept.click()
el_btn_checkout.click()

# Q2
el_btn_del_gem = driver.find_element(By.CSS_SELECTOR, "[data-name='보석 100개']")
assert el_btn_del_gem
el_btn_del_gem.click()

alert = driver.switch_to.alert
print(alert.text) # 창을 닫기 전에 진행
alert.dismiss()


# Q3
el_btns_del = driver.find_elements(By.CLASS_NAME, "cart-row")
print("전체 행의 갯수 :", len(el_btns_del))

el_diplayed_btns = []
for btn in el_btns_del:
    if btn.is_displayed():
        el_diplayed_btns.append(btn)

print("display 행의 갯수 :", len(el_diplayed_btns))

for btn in el_diplayed_btns:
    if "달빛 축제 패키지" in btn.text:
        btn_del = btn.find_element(By.CLASS_NAME, "del-btn")
        btn_del.click()
        break

alert = driver.switch_to.alert
alert.accept()


# Q4
el_btn_gift = driver.find_element(By.ID, "gift-btn")

el_btn_gift.click()
alert = driver.switch_to.alert
alert.send_keys("생일 축하해")
alert.accept()

el_btn_gift.click()
alert = driver.switch_to.alert
alert.accept()

el_btn_gift.click()
alert = driver.switch_to.alert
alert.dismiss()

# Q5
el_btn_stok = driver.find_element(By.ID, "stock-btn")
el_btn_stok.click()

wait = WebDriverWait(driver, 10)
alert = wait.until(
    EC.alert_is_present()
)

print(alert.text)
alert.accept()


input()