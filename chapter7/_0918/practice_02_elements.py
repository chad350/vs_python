""" 실습 2 시작 코드 · 상점 목록 정제와 골드 안에서 쇼핑 계획 """
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



# 이번 실습에서 중요한 포인트

# cards = driver.find_elements(By.CLASS_NAME, "shop-item")               # 없으면 빈 리스트
# price = int("4,800 G".replace(",", "").replace("G", "").strip())           # 4800
# gear = [it for it in items if it["분류"] == "장비"]
# cheapest = min(items, key=lambda it: it["가격"])
# for it in sorted(items, key=lambda it: it["가격"]):                      # 가격이 싼 순서로 반복
#     ...



# 미션 1. 로그인하고 상점 화면으로 이동합니다. (시작 코드에 있습니다.)
driver.get(SITE + "/login.html?reset=1")

login("artia@moon.gg", "artia2026")

wait.until(
    EC.visibility_of_element_located((By.ID, "nav-nick")), 
    "로그인 뒤 닉네임이 보이지 않음"
)
driver.get(SITE + "/shop.html")




# 미션 2. 상점의 카드 10개에서 이름·분류·가격을 읽어 {"이름", "분류", "가격"} 딕셔너리 리스트를 만들고, 건수 문구 「결과 10개」 와 보유 골드 「20,000」 을 정수로 바꿔 읽습니다.
#   확인하려는 것: 화면에 보이는 카드 수와 건수 문구가 서로 맞는지
#   실패 처리: 글자를 정수로 바꾸지 못하면 ValueError 로 멈춥니다.
#   판단 기준: 카드 수와 건수 문구의 숫자가 같음
#   필요한 아이디어
#     ① driver.find_elements 로 카드 리스트 가져오기 (없으면 예외 없이 빈 리스트)
#     ② for card in 카드 리스트: 로 순회하며 card.find_element 로 카드 안에서만 이름·분류·가격 찾기
#     ③ 가격 글자 "12,000 G" 는 문자열 → .replace(",", "").replace("G", "").strip() → int() 로 숫자 변환
#     ④ {"이름": ..., "분류": ..., "가격": ...} 딕셔너리를 만들어 items 리스트에 append
#     ⑤ 건수 문구 "결과 10개" → "결과"·"개" 지우고 strip → int
#     ⑥ 보유 골드 "20,000" → 쉼표 지우고 int

items = []
for card in driver.find_elements(By.CLASS_NAME, "shop-item"):
    price_text = card.find_element(By.CLASS_NAME, "item-price").text
    items.append({
        "이름": card.find_element(By.CLASS_NAME, "item-name").text,
        "분류": card.find_element(By.CLASS_NAME, "item-cat").text,
        "가격": int(price_text.replace(",", "").replace("G", "").strip())
    })

count = int(driver.find_element(By.ID, "result-count").text.replace("결과", "").replace("개", "").strip())
gold = int(driver.find_element(By.ID, "gold").text.replace(",", ""))

print("카드", len(items), "개 / 건수 문구", count, "/ 골드", gold)


# 미션 3. 딕셔너리 리스트로 분류별 이름 목록 {분류: [이름, …]} 과 분류마다 가장 싼 아이템(입문 추천) {분류: 이름} 을 만듭니다.
#   확인하려는 것: 기획서의 입문 추천 아이템이 무엇인지
#   실패 처리: 카드를 하나도 읽지 못했으면 min 에서 ValueError 로 멈추므로, 미션 2 의 카드 수부터 확인합니다.
#   판단 기준: 분류별 이름 수의 합이 10, 입문 추천은 귀환 주문서·모험가 망토·구름 곰
#   필요한 아이디어
#     ① 분류별 이름 목록: 빈 딕셔너리 by_cat 준비 → items 순회 → 분류가 키에 없으면 빈 리스트 만들기 → 이름 append
#     ② 분류마다 그 분류 아이템만 저장: [it for it in items if it["분류"] == cat] (리스트 컴프리헨션)
#     ③ 가장 싼 아이템: min(목록, key=lambda it: it["가격"]) → 결과 딕셔너리의 "이름" 을 cheapest[분류] 에 저장
#     ④ 카드를 하나도 못 읽었으면 min 에서 ValueError → 미션 2 의 카드 수부터 확인



# by_cat
# { 
#   "소모품" : [ "회복 물약", "마나 물약", "해독제" ].
#   "장비" : [ "강철 검", "달빛 검" ],
#   "탈것": ["탈것1", "탈것2", "탈것3"]
# }
by_cat = {}
for it in items:
    cat = it["분류"]
    by_cat.setdefault(cat, [])
    by_cat[cat].append(it["이름"])  


# cheapest
# { 
#   "소모품" : "귀환 주문서",
#   "장비" : "싼 장비",
#   "탈것": "싼 탈것" 
# }
cheapest = {}
for cat in by_cat:
    in_cat = [it for it in items if it["분류"] == cat]
    cheap_item = min(in_cat, key=lambda it: it["가격"])
    cheapest[cat] = cheap_item["이름"]

print("분류별 이름:", by_cat)
print("분류별 가장 싼 아이템:", cheapest)



# 미션 4. 가격이 싼 아이템부터 하나씩 골드에서 차감하며 살 수 있는 아이템 목록을 만들고, 다음 아이템을 살 수 없는 경우에 멈춥니다. 목록의 이름과 가격을 표 모양으로 출력한 뒤 assert 합니다.
#   확인하려는 것: 보유 골드 안에서 살 수 있는 아이템 수를 안내하는 쇼핑 계획
#   실패 처리: 계획 합계가 골드를 넘거나, 다음 아이템을 더해도 골드 안이면 assert 로 멈춥니다.
#   판단 기준: 8개, 합계 17,700 G, 남는 골드 2,300 G, 다음 아이템 「은빛 늑대」 9,000 G 는 부족
#   필요한 아이디어
#     ① 가격이 싼 순서 목록: sorted(items, key=lambda it: it["가격"])
#     ② spent = 0, plan = [], next_item = None 준비
#     ③ 순회하며 spent + 가격 > gold 이면 그 아이템을 next_item 에 저장하고 break
#     ④ 아니면 plan 에 이름 append, spent 에 가격 더하기
#     ⑤ 표 모양 출력: f"{name:<8} {price:>6,} G" 처럼 폭·정렬·쉼표 지정
#     ⑥ assert: spent 가 gold 이하, next_item 가격을 더하면 gold 초과

plan = []
spent = 0
next_item = None

sorted_item = sorted(items, key=lambda it: it["가격"])

for it in sorted_item:
    if spent + it["가격"] > gold:
        next_item = it
        break

    plan.append((it["이름"], it["가격"]))
    spent += it["가격"]

print(f"\n{'구매 계획':<10} {len(plan)}개")

for it in plan:
    name, price = it    
    print(f"  {name:<8} {price:>6,} G")

print(f"합계 {spent:,} G / 남는 골드 {gold - spent:,} G / 다음 아이템 {next_item['이름']} {next_item['가격']:,} G 는 부족")

# 검증
assert len(items) == count and count > 0, f"카드 {len(items)}개 / 건수 문구 {count}"
assert sum(len(v) for v in by_cat.values()) == len(items), f"분류별 이름 수가 전체와 다름: {by_cat}"
assert spent <= gold and (next_item is None or spent + next_item["가격"] > gold), f"계획 합계 {spent} / 골드 {gold}"



input()