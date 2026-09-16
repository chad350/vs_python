import time
import logging
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Chrome()

driver.get("https://302lab.co.kr/websample/selenium-demo/08_%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7")


# mkdir - 디렉토리를 만드는 기능
# parents
#    T - 중간에 빠진 경로가 있어도 처리 (없는 폴더까지 만들어 준다)
#    F - 준간에 빠진 경로가 있으면 에러
# exist_ok
#    T - 이미 해당 폴더가 존재해도 통과
#    F - 이미 해당 폴더가 존재하면 에러

path = "save_data/260916"

Path(path).mkdir(parents=True, exist_ok=True)



# 1. 스크린샷
# 형식 - png
# 텍스트 - 인코딩 
# 이미지 - 인코딩
#   base64 - 일반 png 보다 용량이 좀 크다
#   html, API <- 
# driver.get_screenshot_as_png()
# driver.get_screenshot_as_base64()


# 웹의 화면을 기반을 기반으로 촬영
driver.save_screenshot(f"{path}/test.png")

# 특정한 요소를 기반으로 촬영하는 것
el_props = driver.find_element(By.ID, "prob-card")
el_props.screenshot(f"{path}/card.png")

el_footer = driver.find_element(By.ID, "footer-section")
el_footer.screenshot(f"{path}/footer.png")


# 요 전에 <---  화면을 하단으로 스크롤을 하고 나서 촬영
driver.execute_script("arguments[0].scrollIntoView({block:'center'})", el_footer)
driver.save_screenshot(f"{path}/full_screenshot_foot.png")



# 2. 로그
log_name = f"{path}/log_data.log"
logging.basicConfig(filename=log_name, level=logging.INFO, encoding="utf-8")


logging.info("로그정보를 남깁니다.1")
logging.info("로그정보를 남깁니다.2")
logging.info("로그정보를 남깁니다.3")
logging.info("로그정보를 남깁니다.4")


logging.warning("주의가 필요합니다.")
logging.error("에러가 발생했습니다.")





input()