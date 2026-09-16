import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://302lab.co.kr/websample/selenium-demo/04_%EC%97%AC%EB%9F%AC%EC%B0%BD")

root_handle = driver.current_window_handle

# 새창을 연 후에
# driver 를 해당 창으로 switch 하고 그 이후에 요소에 접근해야함
#   -> NoSuchElementException


# diver close 이후에 switch 를 안하고 사용
#   -> NoSuchWindowException


# iframe 으로 스위치하고 원래 루트페이지에 있는 요소에 접근하려고 할떄
#   -> NoSuchElementException





input()