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

driver.get(SITE + "/shop.html")

# select = Select(driver.find_element(By.ID, "shop-cat"))
# values = [op.get_attribute("value") for op in select.options]        # 고를 수 있는 값
# old = driver.find_element(By.CSS_SELECTOR, "#shop-list .shop-item")   # 누르기 직전에 저장
# driver.find_element(By.ID, "shop-search").click()
# wait.until(EC.staleness_of(old), message="목록이 새로 만들어지지 않음")



# 미션 1. 분류 드롭다운 #shop-cat 에서 고를 수 있는 값을 모두 읽어 리스트로 저장합니다.
#   확인하려는 것: 검색할 분류를 코드에 직접 적지 않고 화면에서 가져오는지
#   실패 처리: 드롭다운을 찾지 못하면 NoSuchElementException 으로 멈춥니다.
#   판단 기준: ['all', '소모품', '장비', '탈것']
#   필요한 아이디어
#     ① 드롭다운(select) 은 Select(driver.find_element(By.ID, "shop-cat")) 로 감싸기
#     ② .options 로 선택지 요소 리스트 가져오기
#     ③ 선택지마다 get_attribute("value") 만 저장: [op.get_attribute("value") for op in 선택지들] (리스트 컴프리헨션)



# 미션 2. 저장한 분류 값마다 검색어를 비우고 검색해서, 결과를 분류 값을 키로 하는 딕셔너리 3개(names_of 이름 목록, cats_of 분류 목록, count_of 건수 문구)에 모읍니다.
#   확인하려는 것: 분류마다 새 검색 결과가 나온 뒤에 읽는지
#   실패 처리: 어느 검색이든 목록이 5초 안에 바뀌지 않으면 조건이 들어간 메시지와 함께 TimeoutException 으로 멈춥니다.
#   판단 기준: 검색마다 이전 카드가 제거된 뒤 읽음
#   필요한 아이디어
#     ① 검색 버튼을 누르면 1.2초 동안 이전 카드가 남아 있음 → 누르기 직전에 카드 하나를 old 에 저장
#     ② 검색 순서: old 저장 → select_by_value(분류) → 검색어 칸 clear() 후 send_keys → 검색 버튼 click → EC.staleness_of(old) 대기
#     ③ 대기가 끝나면 이름·분류 목록을 다시 찾아 리스트 컴프리헨션으로 .text 모으기
#     ④ 같은 순서를 여러 번 쓰므로 검색(검색어, 분류) 함수로 만들고 (이름 목록, 분류 목록, 건수 문구) 반환
#     ⑤ 빈 딕셔너리 names_of·cats_of·count_of 준비 → 분류 값마다 names, cats, count = 검색("", 값) → 세 딕셔너리에 저장



# 미션 3. 모은 결과로 3가지를 판단합니다. ① 분류 결과의 분류가 모두 그 분류인가 ② 건수 문구가 카드 수와 같은가 ③ 소모품·장비·탈것 결과 이름을 합치면 전체 결과 이름과 같은가
#   확인하려는 것: 기획서의 분류 검색·건수 문구·분류와 전체 규칙이 지켜지는지
#   실패 처리: 판단 결과를 변수에 저장하고 마지막에 assert 합니다.
#   판단 기준: 3가지 모두 참
#   필요한 아이디어
#     ① "all" 을 뺀 분류 값만 저장: [v for v in values if v != "all"] (리스트 컴프리헨션)
#     ② 건수 문구 판단: count_of[v] 가 f"결과 {len(names_of[v])}개" 와 다른 분류 값 목록
#     ③ 분류 판단: 분류마다 그 분류가 아닌 분류 글자만 거른 목록 → 개수가 1 이상이면 틀린 분류로 기록
#     ④ 분류 결과 이름을 한 리스트로 합치기 (parts = parts + names_of[v])
#     ⑤ 순서가 다를 수 있으므로 sorted 로 정렬한 뒤 전체 이름 목록과 == 비교



# 미션 4. 분류 「전체」 에서 검색어 목록 ["검", "망토", "알"] 을 차례로 검색하고, 검색어마다 결과 이름과 건수 문구를 읽습니다.
#   확인하려는 것: 결과 이름에 검색어가 모두 들어 있고 건수 문구가 카드 수와 같은지
#   실패 처리: 미션 3 과 같습니다.
#   판단 기준: 검 2개·망토 1개·알 1개, 모든 이름에 검색어가 있음
#   필요한 아이디어
#     ① 검색어 목록 ["검", "망토", "알"] 순회하며 검색(검색어, "all") 호출
#     ② 검색어를 키로 이름 목록·건수 문구를 딕셔너리에 저장
#     ③ 결과가 0개인 검색어 목록 (결과가 0개면 「검색어 없는 이름」 도 0개라 따로 확인해야 함)
#     ④ 검색어마다 [n for n in 이름 목록 if 검색어 not in n] → 개수가 1 이상이면 기록
#     ⑤ 건수 문구가 f"결과 {len(이름 목록)}개" 와 다른 검색어 목록



# 미션 5. 분류 「탈것」 과 검색어 「검」 으로 검색해서 카드 수, 건수 문구, 결과 없음 안내가 보이는지 읽습니다.
#   확인하려는 것: 결과가 없을 때 화면이 기획서대로 표시되는지
#   실패 처리: 미션 3 과 같습니다.
#   판단 기준: 카드 0개, 「결과 0개」, 안내 문구가 보임
#   필요한 아이디어
#     ① 검색("검", "탈것") 호출 (미션 5 의 마지막 결과 카드가 화면에 있어서 old 로 쓸 수 있음)
#     ② 결과 없음 안내는 driver.find_element(By.ID, "empty-msg").is_displayed() 로 확인
#     ③ 결과가 0개가 된 뒤에는 old 로 쓸 카드가 없으므로 이 검색은 마지막에



input()