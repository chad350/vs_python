# import X : X 라는 모듈을 설치하겠다.
# form X import Y : X 라는 모듈의 Y 라는 기능을 가지고 오겠가
import time
from selenium import webdriver


driver = webdriver.Chrome()
driver.get("https://elice.io/")

time.sleep(1)

# 창을 최대 크기로
# driver.maximize_window()

# 창을 최소 크기로
# driver.minimize_window()

# 창을 닫기
# driver.close()

# 뒤로 가기
# driver.back()

# 앞으로 가기
# driver.forward()

# 새로고침
# driver.refresh()


input()