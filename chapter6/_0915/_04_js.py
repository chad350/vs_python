import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://302lab.co.kr/websample/selenium-demo/06_JS%EC%8B%A4%ED%96%89")

# selenium 기능으로 가능한 요소
# 요소를 찾고
# 데이터 읽고
# 데이터를 넣고
# 클릭
# 확인 / 취소

# selenium 기능으로 제한되는 요소
# js 강제로 실행
# excute_script
#  - scroll  ★★★
#  - 날짜 데이터를 전달  ★★★ 
#    send_keys("2026-09-15") - js 강제로 값을 전달   
#  - js 데이터를 확인 ★★ 
#  - 페이지의 상태  ★★
#  - style  ★

# js 를 이용한 값 읽기 - 타이틀, 준비상태
# selenium 에서 실행하기전에 웹에서 console 로 확인하고 진행
# return 이라는 키워드가 있어야 파이썬까지 정보가 돌아옴, 아니면 None
print("제목 [ver.selenium] - ", driver.title)
print("제목 [ver.js] - ", driver.execute_script("return document.title"))
print("페이지의 준비 상태 - ", driver.execute_script("return document.readyState"))


# 스크롤을 실행
# x : 가로  /   y : 세로
# window.scrollTo(x, y)
# window.scrollBy(x, y)
# arguments[0].scrollIntoView({block:'center'})


# 현재 문서의 길이 
# 가로 : document.body.scrollWidth
# 세로 : document.body.scrollHeight

# 현재 스크롤의 위치 
# window.scrollX
# window.scrollY


driver.execute_script("window.scrollBy(0, 200)")
driver.execute_script("window.scrollBy(0, -100)")

print("현재 스크롤의 위치 - ", driver.execute_script("return window.scrollY"))

driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")


# js 기능 - 날짜설정
el_input_start = driver.find_element(By.ID, "start-date")
el_input_start.send_keys("2026-09-15")       # 202609.12 
print(el_input_start.get_attribute("value"))

el_input_end = driver.find_element(By.ID, "end-date")
# argmuents
#                     el_input_date.value = 2026-09-20"
driver.execute_script("arguments[0].value = arguments[1]", el_input_end, "2026-09-20")


# style
driver.execute_script("document.body.style.background = 'red'")



input()