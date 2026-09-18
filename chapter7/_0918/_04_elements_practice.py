""" 실습 1 시작 코드 · 로그인 실패 3가지와 쿠키로 로그인 상태 확인 """
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
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


print("\n=== 1단계. 여러 요소는 find_elements 로 모으고 개수부터 확인합니다 ===")

driver.get(SITE + "/shop.html")

cards = driver.find_elements(By.CLASS_NAME, "shop-item")
names = [ c.find_element(By.CLASS_NAME, "item-name").text for c in cards ]

print(f"찾은 카드의 수 : {len(names)} 개   카드의 이름 : {names}")

print("\n=== 2단계. 카드 안에서 다시 찾으면 같은 아이템의 값끼리 묶이고, 가격은 정수로 바꿔야 계산할 수 있습니다 ===")

# 이름, 분류, 가격
items = []

for c in cards:
    el_name = c.find_element(By.CLASS_NAME, "item-name")
    el_cat = c.find_element(By.CLASS_NAME, "item-cat")
    el_price = c.find_element(By.CLASS_NAME, "item-price")

    # 12,000 G
    price = int(el_price.text.replace(",", "").replace("G", "").strip())

    item = {
        "name"  : el_name.text,
        "cat" : el_cat.text,
        "price" : price
    }

    items.append(item)


print("\n=== 3단계. 조건으로 거르고, key 로 기준을 정해 가장 싼 아이템을 찾습니다 ===")

# 장비만 뽑아서 저장
# [
# {'name': '강철 검', 'cat': '장비', 'price': 2500}, 
# {'name': '달빛 검', 'cat': '장비', 'price': 4800}, 
# {'name': '모험가 망토', 'cat': '장비', 'price': 1800}
# ]
equip_list = [ i for i in items if i["cat"] == "장비" ]

# 장비 가격의 총합
# [2500, 4800, 1800]
price_list = [ e["price"] for e in equip_list]

# 9100
total_price = sum(price_list)

# 모든 아이템 중에서 가장 싼 아이템을 출력
# {'name': '귀환 주문서', 'cat': '소모품', 'price': 150}
cheap_item = min(items, key = lambda i : i["price"])


print("장비 목록 :",equip_list)
print("장비 가격 :",price_list)
print("가격 총합 :",total_price)
print("싼 장비 :",cheap_item)





print(items)
    
    









input()