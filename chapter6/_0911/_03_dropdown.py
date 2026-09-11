import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

driver = webdriver.Chrome()
driver.get("https://302lab.co.kr/websample/selenium-demo/02_%EB%93%9C%EB%A1%AD%EB%8B%A4%EC%9A%B4")

el_dropdonw_server = driver.find_element(By.ID, "server")
dropdown_server = Select(el_dropdonw_server)

# 읽기
print(el_dropdonw_server.text)
print(dropdown_server.first_selected_option.text) # 지금 선택된 옵션

# 쓰기
dropdown_server.select_by_index(0)  # 순서를 통해서 선택
print(dropdown_server.first_selected_option.text)
time.sleep(1)
dropdown_server.select_by_value("jp1") # 태그 옵션 중 value 를 통해서 선택
print(dropdown_server.first_selected_option.text)
time.sleep(1)
dropdown_server.select_by_visible_text("글로벌") # 태그 X -> 눈에 보이는 text 기준으로 선택
print(dropdown_server.first_selected_option.text)


el_dropdown_grade = driver.find_element(By.ID, "grades")
dropdown_grade = Select(el_dropdown_grade)

print(dropdown_grade.is_multiple)

dropdown_grade.select_by_value("normal")
dropdown_grade.select_by_value("vip")
dropdown_grade.select_by_value("vvip")
time.sleep(1)
dropdown_grade.deselect_by_value("normal")
time.sleep(1)
dropdown_grade.deselect_all()




input()

