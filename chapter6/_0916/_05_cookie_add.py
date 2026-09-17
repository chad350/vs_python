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

token_dict = {'domain': '302lab.co.kr', 'expiry': 1790212761, 'httpOnly': False, 'name': 'adv01_op_token', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'OPTK-7A1C'}

driver.add_cookie(token_dict)
driver.refresh()

print(driver.get_cookies())





input()