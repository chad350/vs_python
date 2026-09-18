""" 실습 3 시작 코드 · 분류 드롭다운을 모두 검색하고 결과 검증 """
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

from selenium.webdriver.support import expected_conditions as EC

SITE = "https://302lab.co.kr/websample/game-site"


driver = webdriver.Chrome()                             
wait = WebDriverWait(driver, 5)                         

def login(id, pw):    
    # 이전 시도의 글자가 남아 있을 수 있으므로 clear() 로 비운 뒤 입력합니다
    el_email = driver.find_element(By.ID, "login-email")
    el_email.clear()
    el_email.send_keys(id)

    el_pw = driver.find_element(By.ID, "login-pw")
    el_pw.clear()
    el_pw.send_keys(pw)

    # 로그인 버튼은 누른 뒤 잠시 비활성 상태가 되므로, 누를 수 있을 때까지 기다립니다
    el_login_btn = wait.until(
        EC.element_to_be_clickable((By.ID, "login-btn"))
    )
    el_login_btn.click()


def search(word, category):
    """ 분류와 검색어로 상점을 검색하고 (이름 목록, 분류 목록, 건수 문구) 를 반환합니다

    검색 버튼을 누른 뒤에도 이전 카드가 1.2초 동안 화면에 남아 있습니다.
    그래서 바로 읽으면 이전 결과를 읽게 되므로, 이전 카드가 사라질 때까지 기다린 뒤에 읽습니다.
    """
    # 1. 이전 카드 하나를 미리 저장합니다 (이 카드가 사라지는 것이 검색이 끝난 것으로 판단합니다.)
    el_old_card = driver.find_element(By.CSS_SELECTOR, "#shop-list .shop-item")

    # 2. 드롭다운은 Select 로 감싸야 활용이 가능합니다.
    el_cat = driver.find_element(By.ID, "shop-cat")
    cat_select = Select(el_cat)
    cat_select.select_by_value(category)

    # 3. 검색어 칸에 이전 검색어가 남아 있으므로 clear() 로 비운 뒤 입력합니다
    el_search_box = driver.find_element(By.ID, "shop-q")
    el_search_box.clear()
    el_search_box.send_keys(word)

    el_search_btn = driver.find_element(By.ID, "shop-search")
    el_search_btn.click()

    # 4. 저장해 둔 카드가 사라질 때까지 대기 
    wait.until(
        EC.staleness_of(el_old_card)
    )

    # 5. 목록이 새로 만들어졌으므로 요소를 다시 찾아서 데이터를 확인합니다.
    el_names = driver.find_elements(By.CSS_SELECTOR, "#shop-list .item-name")
    names = [el.text for el in el_names]

    el_cats = driver.find_elements(By.CSS_SELECTOR, "#shop-list .item-cat")
    cats = [el.text for el in el_cats]

    el_count = driver.find_element(By.ID, "result-count")
    count = el_count.text

    # 6. 추출한 데이터를 리턴합니다.
    return names, cats, count


driver.get(SITE + "/login.html?reset=1")                

login("artia@moon.gg", "artia2026")

# 닉네임이 나타나면 로그인이 끝난 것으로 판단
wait.until(
    EC.visibility_of_element_located((By.ID, "nav-nick"))
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

el_cat = driver.find_element(By.ID, "shop-cat")
cat_select = Select(el_cat)                                 # Select 는 요소가 아니라 드롭다운 도우미입니다
el_options = cat_select.options                             # <option> 요소 4개

# 보이는 글자가 아니라 value 속성을 체크
values = [el.get_attribute("value") for el in el_options]

print("분류 값:", values)




# 미션 2. 저장한 분류 값마다 검색어를 비우고 검색해서, 결과를 분류 값을 키로 하는 딕셔너리 3개(names_of 이름 목록, cats_of 분류 목록, count_of 건수 문구)에 모읍니다.
#   확인하려는 것: 분류마다 새 검색 결과가 나온 뒤에 읽는지
#   실패 처리: 어느 검색이든 목록이 5초 안에 바뀌지 않으면 조건이 들어간 메시지와 함께 TimeoutException 으로 멈춥니다.
#   판단 기준: 검색마다 이전 카드가 제거된 뒤 읽음
#   필요한 아이디어
#     ① 검색 버튼을 누르면 1.2초 동안 이전 카드가 남아 있음 → 누르기 직전에 카드 하나를 old 에 저장
#     ② 검색 순서: old 저장 → select_by_value(분류) → 검색어 칸 clear() 후 send_keys → 검색 버튼 click → EC.staleness_of(old) 대기
#     ③ 대기가 끝나면 이름·분류 목록을 다시 찾아 리스트 컴프리헨션으로 .text 모으기
#     ④ 같은 순서를 여러 번 쓰므로 search(검색어, 분류) 함수로 만들고 (이름 목록, 분류 목록, 건수 문구) 반환
#     ⑤ 빈 딕셔너리 names_of·cats_of·count_of 준비 → 분류 값마다 names, cats, count = search("", 값) → 세 딕셔너리에 저장

names_of = {}                                               # {분류 값: 이름 목록}
cats_of = {}                                                # {분류 값: 분류 글자 목록}
count_of = {}                                               # {분류 값: 건수 문구}

for value in values:
    names, cats, count = search("", value)                  # 검색어를 비우고 분류만 바꿔 검색합니다

    names_of[value] = names
    cats_of[value] = cats
    count_of[value] = count

    print(value, " -> ", names, "/", count)




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

categories = [v for v in values if v != "all"]              # 전체를 뺀 분류 값

wrong_count = []                                            # 건수 문구가 카드 수와 다른 분류 값

# 건수 문구는 "all" 을 포함한 모든 분류에서 확인합니다
for value in values:
    expected_count = f"결과 {len(names_of[value])}개"        
    if count_of[value] != expected_count:
        wrong_count.append(value)

wrong_cat = []                                              # 다른 분류가 섞인 분류 값
parts = []                                                  # 분류 결과 이름을 모두 모은 리스트

# 분류가 섞였는지와 이름 합치기는 "all" 을 뺀 분류에서만 확인합니다
for value in categories:
    others = [c for c in cats_of[value] if c != value]      # 이 분류가 아닌 분류 글자 (없어야 정상)

    if len(others) > 0:
        wrong_cat.append(value)

    parts = parts + names_of[value]

# 카드 순서가 다를 수 있으므로 양쪽 모두 정렬한 뒤 비교합니다
same_total = sorted(parts) == sorted(names_of["all"])

print("분류 불일치:", wrong_cat, "/ 건수 문구 불일치:", wrong_count, "/ 분류별 합이 전체와 같음:", same_total)




# 미션 4. 분류 「전체」 에서 검색어 목록 ["검", "망토", "알"] 을 차례로 검색하고, 검색어마다 결과 이름과 건수 문구를 읽습니다.
#   확인하려는 것: 결과 이름에 검색어가 모두 들어 있고 건수 문구가 카드 수와 같은지
#   실패 처리: 미션 3 과 같습니다.
#   판단 기준: 검 2개·망토 1개·알 1개, 모든 이름에 검색어가 있음
#   필요한 아이디어
#     ① 검색어 목록 ["검", "망토", "알"] 순회하며 search(검색어, "all") 호출
#     ② 검색어를 키로 이름 목록·건수 문구를 딕셔너리에 저장
#     ③ 결과가 0개인 검색어 목록 (결과가 0개면 「검색어 없는 이름」 도 0개라 따로 확인해야 함)
#     ④ 검색어마다 [n for n in 이름 목록 if 검색어 not in n] → 개수가 1 이상이면 기록
#     ⑤ 건수 문구가 f"결과 {len(이름 목록)}개" 와 다른 검색어 목록

words = ["검", "망토", "알"]

names_of_word = {}                                          # {검색어: 이름 목록}
count_of_word = {}                                          # {검색어: 건수 문구}

for word in words:
    names, cats, count = search(word, "all")                # 분류는 전체로 두고 검색어만 바꿉니다

    names_of_word[word] = names
    count_of_word[word] = count

    print(word, "→", names, "/", count)

empty_words = []                                            # 결과가 없는 검색어
missing_words = []                                          # 검색어가 없는 이름이 섞인 검색어
wrong_keyword_count = []                                    # 건수 문구가 다른 검색어

for word in words:
    found_names = names_of_word[word]

    # 결과가 0개면 아래 검사가 모두 통과하므로 따로 기록합니다
    if len(found_names) == 0:
        empty_words.append(word)

    without_word = [n for n in found_names if word not in n]    # 검색어가 없는 이름 (없어야 정상)

    if len(without_word) > 0:
        missing_words.append(word)

    expected_count = f"결과 {len(found_names)}개"

    if count_of_word[word] != expected_count:
        wrong_keyword_count.append(word)

print("결과 없음:", empty_words, "/ 검색어 없는 이름:", missing_words, "/ 건수 문구 불일치:", wrong_keyword_count)




# 미션 5. 분류 「탈것」 과 검색어 「검」 으로 검색해서 카드 수, 건수 문구, 결과 없음 안내가 보이는지 읽습니다.
#   확인하려는 것: 결과가 없을 때 화면이 기획서대로 표시되는지
#   실패 처리: 미션 3 과 같습니다.
#   판단 기준: 카드 0개, 「결과 0개」, 안내 문구가 보임
#   필요한 아이디어
#     ① search("검", "탈것") 호출 (미션 4 의 마지막 결과 카드가 화면에 있어서 old 로 쓸 수 있음)
#     ② 결과 없음 안내는 driver.find_element(By.ID, "empty-msg").is_displayed() 로 확인
#     ③ 결과가 0개가 된 뒤에는 old 로 쓸 카드가 없으므로 이 검색은 마지막에

# 결과가 0개가 되면 old 로 쓸 카드가 없으므로 이 검색이 마지막이어야 합니다
empty_names, empty_cats, empty_count = search("검", "탈것")

# 안내 문구는 화면에 항상 있고 숨겨져 있을 뿐이라 is_displayed() 로 확인합니다
el_empty_msg = driver.find_element(By.ID, "empty-msg")
empty_shown = el_empty_msg.is_displayed()

print("탈것 + 검:", empty_names, "/", empty_count, "/ 안내 문구 보임:", empty_shown)



driver.quit()


# 마지막 검증 블록 전체
assert values == ["all", "소모품", "장비", "탈것"], f"분류 값: {values}"
assert len(wrong_cat) == 0, f"분류가 다른 결과: {wrong_cat}"
assert len(wrong_count) == 0, f"건수 문구가 카드 수와 다름: {wrong_count}"
assert same_total, f"분류별 결과 {sorted(parts)} / 전체 {sorted(names_of['all'])}"
assert len(empty_words) == 0, f"결과가 없는 검색어: {empty_words}"
assert len(missing_words) == 0, f"검색어가 없는 이름이 섞인 검색어: {missing_words}"
assert len(wrong_keyword_count) == 0, f"건수 문구 불일치: {wrong_keyword_count}"
assert empty_names == [] and empty_count == "결과 0개" and empty_shown, f"결과 없음 화면: ..."