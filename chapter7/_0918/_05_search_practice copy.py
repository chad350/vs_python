import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

from selenium.webdriver.support import expected_conditions as EC

SITE = "https://302lab.co.kr/websample/game-site"       # 로컬 서버로 실습할 때는 "http://localhost:8640"


driver = webdriver.Chrome()
wait = WebDriverWait(driver, 5)

def login(id, pw):
    email_box = driver.find_element(By.ID, "login-email")
    email_box.clear()
    email_box.send_keys(id)

    pw_box = driver.find_element(By.ID, "login-pw")
    pw_box.clear()
    pw_box.send_keys(pw)

    wait.until(
        EC.element_to_be_clickable((By.ID, "login-btn"))
    ).click()


driver.get(SITE + "/login.html?reset=1")

login("artia@moon.gg", "artia2026")

wait.until(
    EC.visibility_of_element_located((By.ID, "nav-nick")), 
    "로그인 뒤 닉네임이 보이지 않음"
)


print("\n=== 1단계. 검색 버튼을 누른 직후에는 이전 목록이 그대로 남아 있습니다 ===")

driver.get(SITE + "/shop.html")



el_input_search = driver.find_element(By.ID, "shop-q")
el_btn_search = driver.find_element(By.ID, "shop-search")

el_input_search.send_keys("검")
el_btn_search.click()

# 시간
# 요청 완료까지 어느정도의 시간이 걸렸나

prev_time = time.time()

cards = wait.until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "shop-item"))
)

done_time = time.time()

# 요청이 완료되는데까지 걸린 시간
take_time = done_time - prev_time

print(f"찾은 개수 : {len(cards)}   걸린 시간 : {take_time}초")


print("\n=== 2단계. 이전 카드가 제거될 때까지 기다리면 새 검색 결과를 읽을 수 있습니다 ===")

# 기존 요소가 없이지는 것을 기다리는
wait.until(
    EC.staleness_of(cards[-1])
)

el_cards = driver.find_elements(By.CLASS_NAME, "shop-item")

# 요청이 완료되는데까지 걸린 시간
take_time = time.time() - prev_time

print(f"찾은 개수 : {len(el_cards)}   걸린 시간 : {take_time}초")


# 검이라고 검색했을때 -> 결과잘못되었다??
# 검색결과에 검이라는 글자가 없는게 있다면 오류
names = [card.find_element(By.CLASS_NAME, "item-name").text for card in el_cards ]

# names -> 반복을 하면서 이름에 "검" 이라는게 없다면 문제   /  "검" in OOO


el_cat = driver.find_element(By.ID, "shop-cat")
dropdown_cat = Select(el_cat)

# dropdown_cat.options
# dropdown_cat.select_by_visible_text















input()