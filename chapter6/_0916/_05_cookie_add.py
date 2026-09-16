import time
import logging
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Chrome()

driver.get("https://302lab.co.kr/websample/selenium-advanced-demo/a01_admin_login_cookie")


print(driver.get_cookies())

token_dict = { "name": "token", "value" : "asdkjasldkja"}

driver.add_cookie(token_dict)


print(driver.get_cookies())





input()