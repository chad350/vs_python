"""실습 10. 열 제목으로 칸 찾기와 요소 만료 · 정답 코드와 해설

화면 /shop · /inventory        테스트 케이스 8개 (TC-10-01 ~ TC-10-08)

이 실습이 확인하는 것은 3가지입니다.
  ① 칸을 위치 번호가 아니라 열 제목으로 찾으면 열 순서가 바뀌어도 같은 값을 읽는가
  ② 장착하면 표를 다시 만들므로 앞서 받아 둔 요소가 만료되는가
  ③ 장착 여부를 버튼 글자 하나가 아니라 상태 열 · 동작 열 · 장착 요약으로 함께 확인하는가

열 제목 기준 XPath 는 「열 제목 앞의 th 개수 + 1」 로 열 번호를 계산합니다.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from game_login import setup, make_wait, close_dialog, save_screenshot, GAME_URL

# ── 기획 데이터 (화면에서 읽지 않고 기획서 값을 코드에 적습니다)
START_GOLD = 1000
BUY_LIST = [(1, "체력 물약", 50), (11, "견습 단검", 120),
            (12, "사냥꾼의 활", 260), (13, "수호자의 방패", 300)]
PAID = sum([item[2] for item in BUY_LIST])              # 50 + 120 + 260 + 300 = 730
EXPECTED_GOLD = START_GOLD - PAID                       # 1000 - 730 = 270
EXPECTED_ROWS = len(BUY_LIST)

HEADS_A = ["이름", "분류", "등급", "전투력", "상태", "동작"]
HEADS_B = ["상태", "이름", "전투력", "등급", "분류", "동작"]
COLUMNS = ["분류", "등급", "전투력", "상태", "동작"]     # 이름 열은 행을 고르는 데 쓰므로 뺍니다

BOW_NAME = "사냥꾼의 활"
BOW_POWER = "55"
SHIELD_NAME = "수호자의 방패"
DAGGER_NAME = "견습 단검"
BOW_GRADE = "고급"                                      # 열 순서 B 에서 td[4] 로 읽히는 값입니다
POWER_BOW_SHIELD = "100"                                # 55 + 45
POWER_DAGGER_SHIELD = "75"                              # 30 + 45

# 기획서 상점 표를 그대로 옮긴 기대 딕셔너리입니다.
# 처음에는 모두 보관 중이고, 소모품은 전투력과 동작이 모두 - 입니다
SPEC_TABLE_FIRST = {
    "체력 물약": {"분류": "소모품", "등급": "일반", "전투력": "-", "상태": "보관 중", "동작": "-"},
    "견습 단검": {"분류": "무기", "등급": "일반", "전투력": "30", "상태": "보관 중", "동작": "장착"},
    "사냥꾼의 활": {"분류": "무기", "등급": "고급", "전투력": "55", "상태": "보관 중", "동작": "장착"},
    "수호자의 방패": {"분류": "방어구", "등급": "고급", "전투력": "45", "상태": "보관 중", "동작": "장착"}}


def step(title):
    """진행 단계를 출력합니다.

    어느 단계의 값인지 출력에서 구분하기 위해서입니다.
    """
    print(f"\n=== {title} ===")


def to_int(text):
    """화면 글자를 정수로 바꿉니다.

    화면 값은 1,000 처럼 쉼표가 들어 있어 그대로 int() 에 넣으면 ValueError 가 발생합니다.
    """
    return int(text.replace(",", "").strip())


def row_xpath(item_name):
    """아이템 이름으로 표의 행을 고르는 XPath 문자열을 만듭니다.

    행 번호로 고르면 정렬이나 구매 차례가 달라질 때 다른 행을 읽습니다.
    이름 칸은 열 순서가 바뀌어도 class 가 col-name 이라 같은 방법으로 찾습니다.
    """
    return (f"//table[@id='inv-table']/tbody/tr"
            f"[td[@class='col-name'][normalize-space()='{item_name}']]")


def cell_xpath(item_name, col_name):
    """열 제목으로 칸을 고르는 XPath 문자열을 만듭니다 (TC-10-02).

    열 제목 앞에 있는 th 개수를 세고 1을 더하면 그 열의 번호가 됩니다.
    위치 번호를 코드에 적어 두지 않으므로 열 순서가 바뀌어도 같은 칸을 찾습니다.
    """
    column_number = (f"count(//table[@id='inv-table']/thead/tr"
                     f"/th[normalize-space()='{col_name}']/preceding-sibling::th) + 1")
    return row_xpath(item_name) + f"/td[{column_number}]"


def cell_element(driver, item_name, col_name):
    """열 제목 기준으로 칸 요소 1개를 찾습니다.

    XPath 가 칸을 2개 이상 찾으면 첫 칸만 읽고 넘어가 잘못된 값을 확인하게 됩니다.
    개수가 1인지 먼저 보고, 다르면 XPath 를 메시지에 남깁니다.
    """
    xpath = cell_xpath(item_name, col_name)
    found = driver.find_elements(By.XPATH, xpath)
    assert len(found) == 1, f"{item_name} {col_name} 칸 개수: 기대 1, 실제 {len(found)} · {xpath}"
    return found[0]


def read_heads(driver):
    """표의 열 제목을 차례대로 읽습니다."""
    heads = []
    el_heads = driver.find_elements(By.CSS_SELECTOR, "#inv-table thead th")

    for el_head in el_heads:
        heads.append(el_head.text)
    return heads


def read_names(driver):
    """표에 있는 아이템 이름을 표시된 차례대로 읽습니다."""
    names = []
    el_names = driver.find_elements(By.CSS_SELECTOR, "#inv-table td.col-name")

    for el_name in el_names:
        names.append(el_name.text)
    return names


def read_table(driver):
    """표 전체를 {아이템 이름: {열 이름: 값}} 딕셔너리로 모읍니다 (TC-10-02).

    딕셔너리 안에 딕셔너리를 컴프리헨션으로 겹쳐 만들면 어디에서 값이 틀렸는지 알기 어렵습니다.
    바깥은 for 문으로 돌고 안쪽만 한 칸씩 담습니다.
    """
    table = {}
    for item_name in read_names(driver):
        row = {}
        for col_name in COLUMNS:
            row[col_name] = cell_element(driver, item_name, col_name).text
        table[item_name] = row
    return table


def read_td4(driver, item_name):
    """같은 칸을 위치 번호 td[4] 로 읽습니다 (TC-10-03 · TC-10-05).

    비교용으로만 씁니다.
    열 순서가 바뀌면 다른 열이 읽히는 것을 보여 주기 위해서입니다.
    """
    el_cell = driver.find_element(By.XPATH, row_xpath(item_name) + "/td[4]")
    return el_cell.text


def read_summary(driver):
    """장착 요약 3칸(무기 · 방어구 · 장착 전투력)을 딕셔너리로 모읍니다."""
    el_weapon = driver.find_element(By.ID, "equip-weapon")
    el_armor = driver.find_element(By.ID, "equip-armor")
    el_power = driver.find_element(By.ID, "equip-power")
    return {"weapon": el_weapon.text, "armor": el_armor.text, "power": el_power.text}


def row_id_of(driver, item_name):
    """표에서 아이템 이름으로 data-row-id 를 읽습니다.

    장착 버튼 id 는 eq-btn-{row_id} 이므로 번호를 먼저 얻어야 합니다.
    """
    el_row = driver.find_element(By.XPATH, row_xpath(item_name))
    return el_row.get_attribute("data-row-id")


def print_rows(driver_table, names, with_colon):
    """표에서 읽은 행을 출력합니다.

    이름 뒤에 쌍점을 붙일지 여부만 다르므로 함수 하나로 모았습니다.
    """
    for item_name in names:
        mark = ":" if with_colon else ""
        print(f" {item_name}{mark} {driver_table[item_name]}")


# =====================================================================
# 진행
# =====================================================================
driver, _ = setup()
# 장착할 때마다 표를 다시 만드므로 기다리는 시간을 15초로 정한 Wait 를 사용합니다
wait = make_wait(driver, 15)

# ── TC-10-01. 상점에서 4종 구매
step("상점에서 4종 구매")
driver.get(GAME_URL + "/shop")
buy_msgs = []

for item_id, item_name, _price in BUY_LIST:
    el_buy_btn = wait.until(EC.element_to_be_clickable((By.ID, f"buy-btn-{item_id}")),
                            message=f"{item_name} 구매 버튼이 준비되지 않음")
    el_buy_btn.click()
    # wait.until 은 조건을 0.5초 간격으로 다시 실행해 참이 될 때까지 기다립니다.
    # 그래서 인자로 「값」 이 아니라 「호출할 함수」 를 전달해야 합니다.
    #   d.find_element(...).text != ""      ← 지금 시점에서 한 번 계산한 True/False 입니다
    #   lambda d: d.find_element(...).text != ""  ← 회차마다 다시 계산하는 함수입니다
    # lambda 는 이름 없는 함수라 def 로 따로 정의하지 않고 조건 1개를 그대로 작성할 수 있고,
    # 매개변수 d 에는 wait 를 만들 때 지정한 driver 가 회차마다 전달됩니다
    wait.until(lambda d: d.find_element(By.ID, "shop-msg").text != "",
               message=f"{item_name} 구매 결과 문구가 나오지 않음")

    el_shop_msg = driver.find_element(By.ID, "shop-msg")
    buy_msgs.append(el_shop_msg.text)
    # 아이템마다 Dialog 가 열립니다.
    # 닫지 않으면 다음 구매 버튼에서 ElementClickInterceptedException 이 발생합니다
    close_dialog(driver, wait)

print("구매 결과:", buy_msgs)

# ── TC-10-02 · TC-10-03. 열 순서 A 에서 읽기
step("열 순서 A 에서 표 읽기")
driver.get(GAME_URL + "/inventory")
# 반쯤 만들어진 표를 읽으면 행 수가 모자란 목록을 확인하게 됩니다
wait.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, "#inv-table tbody tr")) == EXPECTED_ROWS,
           message="보유 아이템 표가 4행이 되지 않음")

el_hdr_gold = driver.find_element(By.ID, "hdr-gold")
gold_after_buy = to_int(el_hdr_gold.text)
heads_a = read_heads(driver)
table_a = read_table(driver)
names_a = read_names(driver)
td4_a = read_td4(driver, BOW_NAME)
print(f"결제금액 합계 {PAID} · 머리글 골드 {gold_after_buy}")
print("머리글 A:", heads_a)
print_rows(table_a, names_a, False)
print(f"{BOW_NAME} td[4]: {td4_a!r}")

# ── TC-10-04 · TC-10-05. 열 순서를 B 로 바꾼 뒤 같은 함수로 읽기
step("열 순서 B 로 바꾼 뒤 다시 읽기")
el_swap_btn = driver.find_element(By.ID, "inv-swap-btn")
el_swap_btn.click()
# 표시가 바뀌기 전에 읽으면 앞 열 순서의 머리글을 읽습니다
wait.until(lambda d: d.find_element(By.ID, "inv-order").text == "B",
           message="열 순서가 B 로 바뀌지 않음")

heads_b = read_heads(driver)
table_b = read_table(driver)
td4_b = read_td4(driver, BOW_NAME)
el_inv_table = driver.find_element(By.ID, "inv-table")
shot_order_b = save_screenshot(driver, "10_열순서_B", el_inv_table)
print("머리글 B:", heads_b)
print("열 이름 기준 결과가 그대로인가:", table_b == table_a)
print(f"{BOW_NAME} td[4]: {td4_b!r}")

# ── TC-10-06. 열 순서를 A 로 되돌린 뒤 요소 만료 확인
step("장착 뒤 요소 만료 확인")
el_swap_btn = driver.find_element(By.ID, "inv-swap-btn")
el_swap_btn.click()
wait.until(lambda d: d.find_element(By.ID, "inv-order").text == "A",
           message="열 순서가 A 로 되돌아오지 않음")

# 장착 전에 칸 요소를 변수에 받아 둡니다.
# 이 요소가 장착 뒤에 만료되는 것을 확인하려고 먼저 글자도 읽어 둡니다
el_bow_power_before = cell_element(driver, BOW_NAME, "전투력")
power_before_equip = el_bow_power_before.text

el_bow_equip_btn = driver.find_element(By.ID, f"eq-btn-{row_id_of(driver, BOW_NAME)}")
el_bow_equip_btn.click()
wait.until(lambda d: d.find_element(By.ID, "inv-msg").text != "",
           message="장착 결과 문구가 나오지 않음")
el_inv_msg = driver.find_element(By.ID, "inv-msg")
bow_equip_msg = el_inv_msg.text
wait.until(EC.text_to_be_present_in_element((By.ID, "equip-weapon"), BOW_NAME),
           message="장착 무기 글자가 바뀌지 않음")

# 만료를 예외로 확인하는 대신 Wait 조건으로 확인합니다.
# staleness_of 는 그 요소가 더 이상 화면에 없을 때 참이 됩니다
went_stale = wait.until(EC.staleness_of(el_bow_power_before),
                        message="장착 전에 받아 둔 요소가 만료되지 않음")
power_after_equip = cell_element(driver, BOW_NAME, "전투력").text
print(f"{bow_equip_msg} · 장착 전에 받아 둔 요소 글자 {power_before_equip!r}"
      f" · 만료 여부 {went_stale}")
print(f"표를 다시 찾아 읽은 전투력 {power_after_equip!r} (같은 값이지만 요소는 다른 요소입니다)")

# ── TC-10-07. 방어구까지 장착
step("무기와 방어구 장착")
el_shield_equip_btn = driver.find_element(By.ID, f"eq-btn-{row_id_of(driver, SHIELD_NAME)}")
el_shield_equip_btn.click()
wait.until(EC.text_to_be_present_in_element((By.ID, "equip-armor"), SHIELD_NAME),
           message="장착 방어구 글자가 바뀌지 않음")

el_inv_msg = driver.find_element(By.ID, "inv-msg")
shield_equip_msg = el_inv_msg.text
summary_equipped = read_summary(driver)
table_equipped = read_table(driver)
names_equipped = read_names(driver)
print(f"{shield_equip_msg} {summary_equipped}")
print_rows(table_equipped, names_equipped, False)

# ── TC-10-08. 다른 무기로 교체
step("다른 무기로 교체")
el_dagger_equip_btn = driver.find_element(By.ID, f"eq-btn-{row_id_of(driver, DAGGER_NAME)}")
el_dagger_equip_btn.click()
wait.until(EC.text_to_be_present_in_element((By.ID, "equip-weapon"), DAGGER_NAME),
           message="장착 무기가 견습 단검으로 바뀌지 않음")

el_inv_msg = driver.find_element(By.ID, "inv-msg")
dagger_equip_msg = el_inv_msg.text
summary_swapped = read_summary(driver)
table_swapped = read_table(driver)
print(f"{dagger_equip_msg} {summary_swapped}")
print_rows(table_swapped, [BOW_NAME, DAGGER_NAME], True)

driver.quit()


# =====================================================================
# 검증 (브라우저를 닫은 뒤 모아 둔 값을 한꺼번에 비교합니다)
# =====================================================================
# TC-10-01. 결제금액 합계만큼 골드가 줄고 표는 4행입니다
expected_buy_msgs = [f"구매 완료: {item[1]} x1" for item in BUY_LIST]
assert buy_msgs == expected_buy_msgs, f"구매 결과 문구: 기대 {expected_buy_msgs}, 실제 {buy_msgs}"
assert gold_after_buy == EXPECTED_GOLD, \
    f"구매 뒤 머리글 골드: 기대 {EXPECTED_GOLD}, 실제 {gold_after_buy}"

# TC-10-02. 머리글과 표 내용이 기획서 표와 같습니다
assert heads_a == HEADS_A, f"열 순서 A 머리글: 기대 {HEADS_A}, 실제 {heads_a}"
assert table_a == SPEC_TABLE_FIRST, f"열 순서 A 에서 읽은 표: 실제 {table_a}"

# TC-10-03. 열 순서 A 에서 td[4] 는 전투력 열입니다
assert td4_a == BOW_POWER, f"열 순서 A 의 td[4]: 기대 {BOW_POWER!r}(전투력 열), 실제 {td4_a!r}"

# TC-10-04. 열 순서를 바꾸면 머리글 차례가 달라집니다
assert heads_b == HEADS_B, f"열 순서 B 머리글: 기대 {HEADS_B}, 실제 {heads_b}"

# TC-10-05. 열 이름 기준 결과는 그대로이고, 위치 번호 기준 결과만 달라집니다
assert table_b == table_a, f"열 이름 기준 결과: 기대 A 와 같음, 실제 {table_b}"
assert td4_b == BOW_GRADE, f"열 순서 B 의 td[4]: 기대 {BOW_GRADE!r}(등급 열), 실제 {td4_b!r}"
assert td4_a != td4_b, f"위치 번호로 찾은 두 값: 기대 서로 다름, 실제 {td4_a!r}·{td4_b!r}"

# TC-10-06. 장착 전에 받아 둔 요소는 만료되고, 다시 찾아 읽은 값은 같습니다
assert went_stale is True, f"장착 전에 받아 둔 요소: 기대 만료, 실제 {went_stale}"
assert power_after_equip == power_before_equip == BOW_POWER, \
    (f"다시 찾아 읽은 전투력: 기대 {BOW_POWER!r}, "
     f"실제 {power_before_equip!r} → {power_after_equip!r}")

# TC-10-07. 장착 여부는 상태 열 · 동작 열 · 장착 요약을 같이 읽어 판정합니다
assert summary_equipped == {"weapon": BOW_NAME, "armor": SHIELD_NAME, "power": POWER_BOW_SHIELD}, \
    (f"장착 요약: 기대 {BOW_NAME}·{SHIELD_NAME}·{POWER_BOW_SHIELD}, "
     f"실제 {summary_equipped}")

# 기대와 다른 행만 모아 개수로 판정하면 어느 행이 달랐는지 메시지에 남습니다
equipped_expected = {BOW_NAME: "장착 중", SHIELD_NAME: "장착 중",
                     DAGGER_NAME: "보관 중", "체력 물약": "보관 중"}
wrong_states = [name for name in equipped_expected
                if table_equipped[name]["상태"] != equipped_expected[name]]
assert len(wrong_states) == 0, f"장착 뒤 상태 열이 다른 행: {wrong_states} · {table_equipped}"
assert table_equipped[BOW_NAME]["동작"] == "해제", \
    f"장착한 무기 행의 동작: 기대 '해제', 실제 {table_equipped[BOW_NAME]['동작']!r}"
assert table_equipped["체력 물약"]["전투력"] == "-" and table_equipped["체력 물약"]["동작"] == "-", \
    f"소모품 행: 기대 전투력·동작 모두 '-', 실제 {table_equipped['체력 물약']}"

# TC-10-08. 무기를 바꾸면 앞 무기가 자동으로 해제되어 보관 중으로 돌아옵니다
assert table_swapped[BOW_NAME]["상태"] == "보관 중" and table_swapped[BOW_NAME]["동작"] == "장착", \
    (f"무기 교체 뒤 {BOW_NAME}: 기대 상태 '보관 중'·동작 '장착', "
     f"실제 {table_swapped[BOW_NAME]}")
assert summary_swapped == {"weapon": DAGGER_NAME, "armor": SHIELD_NAME, "power": POWER_DAGGER_SHIELD}, \
    (f"무기 교체 뒤 장착 요약: 기대 {DAGGER_NAME}·{SHIELD_NAME}·{POWER_DAGGER_SHIELD}, "
     f"실제 {summary_swapped}")

# 없는 파일만 모아 개수로 판정하면 어느 스크린샷이 없는지 메시지에 남습니다
import os
missing_shots = [path for path in [shot_order_b] if not os.path.exists(path)]
assert len(missing_shots) == 0, f"스크린샷이 없습니다: {missing_shots}"

print("게임 실습 10 정답 통과")
