import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("https://302lab.co.kr/websample/selenium/03-login/")


input_id = driver.find_element(By.NAME, "username")
input_pw = driver.find_element(By.NAME, "password")
input_id.send_keys("test_user")
input_pw.send_keys("1234")

btn_login = driver.find_element(By.ID, "loginBtn")
btn_login.click()

input()