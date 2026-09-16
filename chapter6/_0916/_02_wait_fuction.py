import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

driver.get("https://302lab.co.kr/websample/selenium-demo/05_%EB%8F%99%EA%B8%B0%ED%99%94")

# wait

# 셀레니움 - 무한스크롤 자동화
# 1. 스크롤 - excute_script
# 스크르롤을 맨 아래까지 내릴것

# 2. 대기
# ????
# selenium EC - 어떤 요소가 뜬다, 나타단다, 클릭한상태가 된다
# EC 커버가 안되는 것은 직접 만든 함수로 제어할 수 있다.



# wait 로 전달할 함수의 조건
# 1 - 매개변수
#  - 꼭 1개 받아야한다.
#  - driver
# 2 - return
#  - bool 형태

# 주기적으로 실행이 된다. (0.5)

# count = 0
# def test_func(d):
#     global count
#     count += 1

#     print("대기중입니다. ", count)

#     return count > 3

wait = WebDriverWait(driver, 3)

# 함수실행

def check_scroll(d):
    # 1. 스크립트를 하단으로 내린다.
    d.execute_script("window.scrollTo(0, document.body.scrollHeight)")

    # 2. "log-item" 을 클래스로 가진 요소의 개수 체크
    items = d.find_elements(By.CLASS_NAME, "log-item")

    print(f"크롤링 중입니다. 수집데이터 : {len(items)}건")

    # 3. 개수가 12가 넘어가면 완료다 
    return len(items) >= 12

wait.until(
    check_scroll
)

items = driver.find_elements(By.CLASS_NAME, "log-item")
print("로그의 개수 :", len(items))


input()