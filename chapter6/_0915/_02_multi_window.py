import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://302lab.co.kr/websample/selenium-demo/04_%EC%97%AC%EB%9F%AC%EC%B0%BD")

root_handle = driver.current_window_handle

# 지금 열린 윈도우의 수
print("handle count :", len(driver.window_handles))

el_btn_link = driver.find_element(By.LINK_TEXT, "새 창으로 보기")
el_btn_link.click()

# el_terms = driver.find_element(By.ID, "terms")    기존 창의 정보 - 찾을 수 있다.
# el_detail_name = driver.find_element(By.ID, "detail-name")   새로운 창의 정보 - 찾을 수 없음

# 지금 열린 (driver 기준) 의 제목
print("title :", driver.title)

# 지금 열린 handle - 내부적으로 관리하는 id
print("handle :", driver.current_window_handle)

# 지금 열린 윈도우의 수
print("handle count :", len(driver.window_handles))

print("#####################")

for handle in driver.window_handles:
    if handle == root_handle:
        print(f"{handle} 은 지금 열린 페이지의 핸들입니다.")
    else : 
        print(f"{handle} 은 지금 열리지 않은 페이지의 핸들입니다.")
        # window 를 통해 전환을 핸들값
        driver.switch_to.window(handle)    
        print("창을 전환합니다.")

print("#####################")

# 지금 열린 (driver 기준) 의 제목
print("title :", driver.title)
# 지금 열린 handle - 내부적으로 관리하는 id
print("handle :", driver.current_window_handle)

# 현재 driver 가 가르키는 윈도우를 닫는 것 -> 창이 여러개면 1개만 닫는 것
# driver.close()
driver.switch_to.window(root_handle)



el_btn_terms = driver.find_element(By.ID, "terms-btn")
el_btn_terms.click()

# 윈도우가 뜰때 확인하는 wait
wait = WebDriverWait(driver, 10)
wait.until(
    EC.number_of_windows_to_be(2)
)

print("handle count :", len(driver.window_handles))
for handle in driver.window_handles:
    if handle == root_handle:
        print(f"{handle} 은 지금 열린 페이지의 핸들입니다.")
    else : 
        print(f"{handle} 은 지금 열리지 않은 페이지의 핸들입니다.")
        driver.switch_to.window(handle)    
        print("창을 전환합니다.")


el_terms_title = driver.find_element(By.ID, "terms-title")
print(el_terms_title.text)

driver.close()
driver.switch_to.window(root_handle)    

print(driver.title)

input()