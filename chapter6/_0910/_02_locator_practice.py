import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("https://302lab.co.kr/websample/css-selector/")

# id
# 로그인 버튼

# tag
# 제목
# 버튼 - 3개

# name
# 검색창 input

# class
# item 

# link text, p link text
# 정확히 -> 거래명세서
# 보고서가 포함된 내용 찾기

# css selecot
# 태그  아이디   클래스    속성
#       #      .       []
#                    시작  ^
#                    끝   $
#                    포함  *


# 아이디가 email 이 포함
result_1 = driver.find_element(By.CSS_SELECTOR, "[id*='email']")
print(result_1.text)

# 검색 창중에 search 가 포함
result_2 = driver.find_element(By.CSS_SELECTOR, "[data-testid*='search']")
print(result_2.text)


# id 가 _7a3f 로 끝나는 것
result_3 = driver.find_elements(By.CSS_SELECTOR, "[id$='_7a3f']")
print(len(result_3))

# id 가 user 로 시작
result_4 = driver.find_elements(By.CSS_SELECTOR, "[id^='user']")
print(len(result_4))


# 상품 목록 안의 span
result_5 = driver.find_elements(By.CSS_SELECTOR, ".product-list span")

# 주문 내역에서 결제완료
result_6 = driver.find_elements(By.CSS_SELECTOR, "[data-status='paid']")

print(len(result_5))
print(len(result_6))


# xpath
# 로그인 버튼을 - id
driver.find_element(By.ID, "btn_login_7a3f")
result_7 = driver.find_element(By.XPATH, "//button[@id='btn_login_7a3f']")

# product list [ul] - id
driver.find_element(By.ID, "productList")
result_8 = driver.find_element(By.XPATH, "//ul[@id='productList']")

print(result_7.tag_name)
print(result_8.tag_name)



# driver.find_element() -> text
# driver.find_elements() -> len()



input()