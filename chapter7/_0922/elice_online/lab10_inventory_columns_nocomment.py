from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from game_login import setup, make_wait, close_dialog, save_screenshot, GAME_URL

START_GOLD = 1000
BUY_LIST = [(1, "체력 물약", 50), (11, "견습 단검", 120),
            (12, "사냥꾼의 활", 260), (13, "수호자의 방패", 300)]
PAID = sum([item[2] for item in BUY_LIST])
EXPECTED_GOLD = START_GOLD - PAID
EXPECTED_ROWS = len(BUY_LIST)

HEADS_A = ["이름", "분류", "등급", "전투력", "상태", "동작"]
HEADS_B = ["상태", "이름", "전투력", "등급", "분류", "동작"]
COLUMNS = ["분류", "등급", "전투력", "상태", "동작"]

BOW_NAME = "사냥꾼의 활"
BOW_POWER = "55"
SHIELD_NAME = "수호자의 방패"
DAGGER_NAME = "견습 단검"
BOW_GRADE = "고급"
POWER_BOW_SHIELD = "100"
POWER_DAGGER_SHIELD = "75"

SPEC_TABLE_FIRST = {
    "체력 물약": {"분류": "소모품", "등급": "일반", "전투력": "-", "상태": "보관 중", "동작": "-"},
    "견습 단검": {"분류": "무기", "등급": "일반", "전투력": "30", "상태": "보관 중", "동작": "장착"},
    "사냥꾼의 활": {"분류": "무기", "등급": "고급", "전투력": "55", "상태": "보관 중", "동작": "장착"},
    "수호자의 방패": {"분류": "방어구", "등급": "고급", "전투력": "45", "상태": "보관 중", "동작": "장착"}}


def step(title):
    print(f"\n=== {title} ===")


def to_int(text):
    return int(text.replace(",", "").strip())


def row_xpath(item_name):
    return (f"//table[@id='inv-table']/tbody/tr"
            f"[td[@class='col-name'][normalize-space()='{item_name}']]")


def cell_xpath(item_name, col_name):
    column_number = (f"count(//table[@id='inv-table']/thead/tr"
                     f"/th[normalize-space()='{col_name}']/preceding-sibling::th) + 1")
    return row_xpath(item_name) + f"/td[{column_number}]"


def cell_element(driver, item_name, col_name):
    xpath = cell_xpath(item_name, col_name)
    found = driver.find_elements(By.XPATH, xpath)
    assert len(found) == 1, f"{item_name} {col_name} 칸 개수: 기대 1, 실제 {len(found)} · {xpath}"
    return found[0]


def read_heads(driver):
    heads = []
    el_heads = driver.find_elements(By.CSS_SELECTOR, "#inv-table thead th")

    for el_head in el_heads:
        heads.append(el_head.text)
    return heads


def read_names(driver):
    names = []
    el_names = driver.find_elements(By.CSS_SELECTOR, "#inv-table td.col-name")

    for el_name in el_names:
        names.append(el_name.text)
    return names


def read_table(driver):
    table = {}
    for item_name in read_names(driver):
        row = {}
        for col_name in COLUMNS:
            row[col_name] = cell_element(driver, item_name, col_name).text
        table[item_name] = row
    return table


def read_td4(driver, item_name):
    el_cell = driver.find_element(By.XPATH, row_xpath(item_name) + "/td[4]")
    return el_cell.text


def read_summary(driver):
    el_weapon = driver.find_element(By.ID, "equip-weapon")
    el_armor = driver.find_element(By.ID, "equip-armor")
    el_power = driver.find_element(By.ID, "equip-power")
    return {"weapon": el_weapon.text, "armor": el_armor.text, "power": el_power.text}


def row_id_of(driver, item_name):
    el_row = driver.find_element(By.XPATH, row_xpath(item_name))
    return el_row.get_attribute("data-row-id")


def print_rows(driver_table, names, with_colon):
    for item_name in names:
        mark = ":" if with_colon else ""
        print(f" {item_name}{mark} {driver_table[item_name]}")


driver, _ = setup()
wait = make_wait(driver, 15)

step("상점에서 4종 구매")
driver.get(GAME_URL + "/shop")
buy_msgs = []

for item_id, item_name, _price in BUY_LIST:
    el_buy_btn = wait.until(EC.element_to_be_clickable((By.ID, f"buy-btn-{item_id}")),
                            message=f"{item_name} 구매 버튼이 준비되지 않음")
    el_buy_btn.click()
    wait.until(lambda d: d.find_element(By.ID, "shop-msg").text != "",
               message=f"{item_name} 구매 결과 문구가 나오지 않음")

    el_shop_msg = driver.find_element(By.ID, "shop-msg")
    buy_msgs.append(el_shop_msg.text)
    close_dialog(driver, wait)

print("구매 결과:", buy_msgs)

step("열 순서 A 에서 표 읽기")
driver.get(GAME_URL + "/inventory")
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

step("열 순서 B 로 바꾼 뒤 다시 읽기")
el_swap_btn = driver.find_element(By.ID, "inv-swap-btn")
el_swap_btn.click()
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

step("장착 뒤 요소 만료 확인")
el_swap_btn = driver.find_element(By.ID, "inv-swap-btn")
el_swap_btn.click()
wait.until(lambda d: d.find_element(By.ID, "inv-order").text == "A",
           message="열 순서가 A 로 되돌아오지 않음")

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

went_stale = wait.until(EC.staleness_of(el_bow_power_before),
                        message="장착 전에 받아 둔 요소가 만료되지 않음")
power_after_equip = cell_element(driver, BOW_NAME, "전투력").text
print(f"{bow_equip_msg} · 장착 전에 받아 둔 요소 글자 {power_before_equip!r}"
      f" · 만료 여부 {went_stale}")
print(f"표를 다시 찾아 읽은 전투력 {power_after_equip!r} (같은 값이지만 요소는 다른 요소입니다)")

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


expected_buy_msgs = [f"구매 완료: {item[1]} x1" for item in BUY_LIST]
assert buy_msgs == expected_buy_msgs, f"구매 결과 문구: 기대 {expected_buy_msgs}, 실제 {buy_msgs}"
assert gold_after_buy == EXPECTED_GOLD, \
    f"구매 뒤 머리글 골드: 기대 {EXPECTED_GOLD}, 실제 {gold_after_buy}"

assert heads_a == HEADS_A, f"열 순서 A 머리글: 기대 {HEADS_A}, 실제 {heads_a}"
assert table_a == SPEC_TABLE_FIRST, f"열 순서 A 에서 읽은 표: 실제 {table_a}"

assert td4_a == BOW_POWER, f"열 순서 A 의 td[4]: 기대 {BOW_POWER!r}(전투력 열), 실제 {td4_a!r}"

assert heads_b == HEADS_B, f"열 순서 B 머리글: 기대 {HEADS_B}, 실제 {heads_b}"

assert table_b == table_a, f"열 이름 기준 결과: 기대 A 와 같음, 실제 {table_b}"
assert td4_b == BOW_GRADE, f"열 순서 B 의 td[4]: 기대 {BOW_GRADE!r}(등급 열), 실제 {td4_b!r}"
assert td4_a != td4_b, f"위치 번호로 찾은 두 값: 기대 서로 다름, 실제 {td4_a!r}·{td4_b!r}"

assert went_stale is True, f"장착 전에 받아 둔 요소: 기대 만료, 실제 {went_stale}"
assert power_after_equip == power_before_equip == BOW_POWER, \
    (f"다시 찾아 읽은 전투력: 기대 {BOW_POWER!r}, "
     f"실제 {power_before_equip!r} → {power_after_equip!r}")

assert summary_equipped == {"weapon": BOW_NAME, "armor": SHIELD_NAME, "power": POWER_BOW_SHIELD}, \
    (f"장착 요약: 기대 {BOW_NAME}·{SHIELD_NAME}·{POWER_BOW_SHIELD}, "
     f"실제 {summary_equipped}")

equipped_expected = {BOW_NAME: "장착 중", SHIELD_NAME: "장착 중",
                     DAGGER_NAME: "보관 중", "체력 물약": "보관 중"}
wrong_states = [name for name in equipped_expected
                if table_equipped[name]["상태"] != equipped_expected[name]]
assert len(wrong_states) == 0, f"장착 뒤 상태 열이 다른 행: {wrong_states} · {table_equipped}"
assert table_equipped[BOW_NAME]["동작"] == "해제", \
    f"장착한 무기 행의 동작: 기대 '해제', 실제 {table_equipped[BOW_NAME]['동작']!r}"
assert table_equipped["체력 물약"]["전투력"] == "-" and table_equipped["체력 물약"]["동작"] == "-", \
    f"소모품 행: 기대 전투력·동작 모두 '-', 실제 {table_equipped['체력 물약']}"

assert table_swapped[BOW_NAME]["상태"] == "보관 중" and table_swapped[BOW_NAME]["동작"] == "장착", \
    (f"무기 교체 뒤 {BOW_NAME}: 기대 상태 '보관 중'·동작 '장착', "
     f"실제 {table_swapped[BOW_NAME]}")
assert summary_swapped == {"weapon": DAGGER_NAME, "armor": SHIELD_NAME, "power": POWER_DAGGER_SHIELD}, \
    (f"무기 교체 뒤 장착 요약: 기대 {DAGGER_NAME}·{SHIELD_NAME}·{POWER_DAGGER_SHIELD}, "
     f"실제 {summary_swapped}")

import os
missing_shots = [path for path in [shot_order_b] if not os.path.exists(path)]
assert len(missing_shots) == 0, f"스크린샷이 없습니다: {missing_shots}"

print("게임 실습 10 정답 통과")
