import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://302lab.co.kr/websample/selenium-control/p4_결제창")

root_handle = driver.current_window_handle

# Q1
# 페이지가 바뀌기 전
el_btn_open_pg = driver.find_element(By.ID, "open-pg-btn")
el_btn_open_pg.click()

order_name = driver.find_element(By.ID, "order-name").text
order_amount = driver.find_element(By.ID, "order-amount").text

wait = WebDriverWait(driver, 10)
wait.until(
    EC.number_of_windows_to_be(2)
)

print("열린 윈도우 갯수 :", len(driver.window_handles))

for handle in driver.window_handles:
    if handle == root_handle:
        print(f"{handle} 는 루트 핸들입니다.")
    else:
        print(f"{handle} 는 루트 핸들이 아닙니다..")
        driver.switch_to.window(handle)
        print("driver 타겟 window 전환")


# 페이지가 바뀌고 나서 이후
print("타이틀 : ", driver.title)

el_pg_item = driver.find_element(By.ID, "pg-item")
el_pg_amount = driver.find_element(By.ID, "pg-amount")

assert order_name == el_pg_item.text, "상품이 다릅니다."
assert order_amount == el_pg_amount.text, "상품 가격이 다릅니다."


# Q2
driver.close()
driver.switch_to.window(root_handle)

el_summary = driver.find_element(By.ID, "summary")
el_first_p = el_summary.find_element(By.TAG_NAME, "p")

print("열린 윈도우 갯수 -", len(driver.window_handles))
print("주문 요약 -", el_first_p.text)



input()