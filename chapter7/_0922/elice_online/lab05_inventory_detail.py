"""실습 5. 인벤토리 상세 패널 동기화 · 정답 코드와 해설

화면 /shop · /inventory        테스트 케이스 8개 (TC-5-01 ~ TC-5-08)

이 실습이 확인하는 것은 3가지입니다.
  ① 가방 칸을 고르기만 했을 때 상세만 바뀌고 장착은 되지 않는가
  ② 장착하면 상세 · 표 · 장착 요약 · 보정값이 같은 값으로 함께 움직이는가
  ③ 분류 거르기가 가방 칸만 줄이고 표의 행 수는 그대로 두는가

읽은 값은 읽는 즉시 판단하지 않고 변수에 모아 두고, 브라우저를 닫은 뒤 마지막에 한꺼번에 비교합니다.
중간에 assert 로 멈추면 남은 화면을 확인하지 못하고 스크린샷도 남지 않기 때문입니다.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from game_login import setup, make_wait, close_dialog, save_screenshot, GAME_URL

# ── 기획 데이터 (화면에서 읽지 않고 기획서 값을 코드에 적습니다)
START_GOLD = 1000
BUY_LIST = [(1, "체력 물약", 50), (11, "견습 단검", 120), (12, "사냥꾼의 활", 260), (13, "수호자의 방패", 300)]
BOW_NAME = "사냥꾼의 활"
BOW_POWER = 55
SHIELD_NAME = "수호자의 방패"
SHIELD_POWER = 45
DAGGER_NAME = "견습 단검"
DAGGER_POWER = 30
POTION_NAME = "체력 물약"
EXPECTED_GOLD = START_GOLD - sum([item[2] for item in BUY_LIST])      # 1000 - 730 = 270
EXPECTED_ROWS = len(BUY_LIST)
FILTER_COUNTS = {"무기": 2, "방어구": 1, "소모품": 1, "전체": 4}        # 거르기별 가방 칸 수


def row_xpath(name):
    """아이템 이름으로 표의 행을 고르는 XPath 문자열을 만듭니다.

    행 번호로 고르면 정렬이나 구매 차례가 달라질 때 다른 행을 읽습니다.
    이름 칸의 글자로 고르면 행 순번이 달라져도 같은 아이템을 찾습니다.
    """
    return f"//table[@id='inv-table']/tbody/tr[td[@class='col-name'][normalize-space()='{name}']]"


def row_id_of(driver, name):
    """표에서 아이템 이름으로 data-row-id 를 읽습니다.

    가방 칸에는 id 가 없고 data-row-id 만 있습니다.
    표와 가방이 같은 번호를 사용하므로, 표에서 번호를 얻어 가방 칸을 찾습니다.
    """
    el_row = driver.find_element(By.XPATH, row_xpath(name))
    return el_row.get_attribute("data-row-id")


def table_state(driver, name):
    """그 아이템 행의 상태 칸 글자를 반환합니다."""
    el_state = driver.find_element(By.XPATH, row_xpath(name) + "/td[@class='col-state']")
    return el_state.text


def select_slot(driver, wait, name):
    """가방 칸을 눌러 상세 패널을 그 아이템으로 바꿉니다 (TC-5-02)."""
    el_slot = driver.find_element(
        By.CSS_SELECTOR, f'#bag-grid .item-slot[data-row-id="{row_id_of(driver, name)}"]')
    el_slot.click()
    # 누른 직후 상세를 읽으면 앞 아이템의 값을 그대로 읽습니다.
    # 제목이 그 아이템 이름이 되는 것을 신호로 삼아 다음 동작으로 갑니다.
    wait.until(EC.text_to_be_present_in_element((By.ID, "detail-title"), name),
               message=f"상세 패널이 {name} 으로 바뀌지 않음")


def read_detail(driver):
    """상세 패널의 값 8가지를 딕셔너리 하나로 모읍니다."""
    el_title = driver.find_element(By.ID, "detail-title")
    el_rarity = driver.find_element(By.ID, "detail-rarity")
    el_kind = driver.find_element(By.ID, "detail-kind")
    el_state = driver.find_element(By.ID, "detail-state")
    el_power = driver.find_element(By.ID, "detail-power")
    el_difference = driver.find_element(By.ID, "detail-difference")
    el_equip_btn = driver.find_element(By.ID, "detail-equip-btn")

    return {"name": el_title.text,
            "grade": el_rarity.text,
            "kind": el_kind.text,
            "state": el_state.text,
            "power": el_power.text,
            "change": el_difference.text,
            "btn_text": el_equip_btn.text,
            "btn_enabled": el_equip_btn.is_enabled()}


def read_summary(driver):
    """장착 요약 3칸(무기 · 방어구 · 장착 전투력)을 딕셔너리로 모읍니다."""
    el_weapon = driver.find_element(By.ID, "equip-weapon")
    el_armor = driver.find_element(By.ID, "equip-armor")
    el_power = driver.find_element(By.ID, "equip-power")
    return {"weapon": el_weapon.text, "armor": el_armor.text, "power": el_power.text}


def visible_slot_count(driver):
    """지금 보이는 가방 칸 수를 셉니다."""
    el_slots = driver.find_elements(By.CSS_SELECTOR, "#bag-grid .item-slot")
    return len(el_slots)


# =====================================================================
# 진행
# =====================================================================
driver, _ = setup()
# 장착할 때마다 표와 가방을 다시 만들므로 기다리는 시간을 15초로 정한 Wait 를 사용합니다
wait = make_wait(driver, 15)

# ── TC-5-01. 상점에서 4종 구매
driver.get(GAME_URL + "/shop")
for item_id, name, price in BUY_LIST:
    el_buy_btn = wait.until(EC.element_to_be_clickable((By.ID, f"buy-btn-{item_id}")),
                            message=f"{name} 구매 버튼을 누를 수 없음")
    el_buy_btn.click()
    # 결과 문구에 이름이 들어오는 것을 조건으로 사용합니다.
    # 「빈 글자가 아님」 만 조건으로 두면 앞 아이템의 문구를 새 결과로 읽습니다.
    wait.until(EC.text_to_be_present_in_element((By.ID, "shop-msg"), name),
               message=f"{name} 구매 결과 문구가 나오지 않음")
    # 아이템마다 Dialog 가 열립니다.
    # 닫지 않으면 다음 구매 버튼에서 ElementClickInterceptedException 이 납니다
    close_dialog(driver, wait)

driver.get(GAME_URL + "/inventory")
# wait.until 은 조건을 0.5초 간격으로 다시 실행해 참이 될 때까지 기다립니다.
# 그래서 인자로 「값」 이 아니라 「호출할 함수」 를 전달해야 합니다.
#   len(driver.find_elements(...)) == 4      ← 지금 시점에서 한 번 계산한 True/False 입니다
#   lambda d: len(d.find_elements(...)) == 4 ← 회차마다 다시 세는 함수입니다
# lambda 는 이름 없는 함수라 def 로 따로 정의하지 않고 조건 1개를 그대로 작성할 수 있고,
# 매개변수 d 에는 wait 를 만들 때 지정한 driver 가 회차마다 전달됩니다
wait.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, "#inv-table tbody tr")) == EXPECTED_ROWS,
           message="인벤토리 4행이 표시되지 않음")

el_header_gold = driver.find_element(By.ID, "hdr-gold")
header_gold_text = el_header_gold.text

# ── TC-5-02 · TC-5-03. 가방 칸을 고른 직후의 상세와 장착 요약
select_slot(driver, wait, BOW_NAME)
detail_selected = read_detail(driver)
# 고르기만 하고 장착됐다고 판정하기 쉬우므로, 같은 시점의 장착 요약을 따로 읽어 둡니다
summary_selected = read_summary(driver)

# ── TC-5-04. 상세에서 장착
el_equip_btn = driver.find_element(By.ID, "detail-equip-btn")
el_equip_btn.click()
# 장착 무기 글자가 그 이름이 되는 것을 신호로 삼습니다.
# 기다리지 않으면 장착 전 요약을 읽습니다
wait.until(EC.text_to_be_present_in_element((By.ID, "equip-weapon"), BOW_NAME),
           message="무기가 장착되지 않음")

detail_equipped = read_detail(driver)
summary_equipped = read_summary(driver)
bow_state_equipped = table_state(driver, BOW_NAME)

el_inv_msg = driver.find_element(By.ID, "inv-msg")
equip_msg = el_inv_msg.text
el_weapon_slot = driver.find_element(By.ID, "slot-weapon")
weapon_slot_class = el_weapon_slot.get_attribute("class")
el_weapon_power = driver.find_element(By.ID, "weapon-power")
weapon_bonus = el_weapon_power.text

# ── TC-5-05. 방어구까지 장착해 전투력 합계 확인
# 표의 장착 버튼은 id 에 행 번호가 들어가므로 이름으로 번호를 먼저 얻습니다
el_shield_btn = driver.find_element(By.ID, "eq-btn-" + row_id_of(driver, SHIELD_NAME))
el_shield_btn.click()
wait.until(EC.text_to_be_present_in_element((By.ID, "equip-armor"), SHIELD_NAME),
           message="방어구가 장착되지 않음")
summary_both = read_summary(driver)

# ── TC-5-06. 다른 무기로 교체
select_slot(driver, wait, DAGGER_NAME)
# 예고는 교체하기 전에 읽어야 합니다.
# 교체 뒤에는 이 값이 사라집니다
swap_preview = read_detail(driver)["change"]

el_dagger_equip_btn = driver.find_element(By.ID, "detail-equip-btn")
el_dagger_equip_btn.click()
wait.until(EC.text_to_be_present_in_element((By.ID, "equip-weapon"), DAGGER_NAME),
           message="무기가 견습 단검으로 바뀌지 않음")

summary_swapped = read_summary(driver)
# 표를 다시 만들었으므로 앞에서 찾아 둔 요소는 사용하지 않고 이름으로 다시 찾습니다
bow_state_swapped = table_state(driver, BOW_NAME)
shot_swapped = save_screenshot(driver, "05_무기_교체_뒤")

# ── TC-5-07. 분류 거르기
filter_counts = {}
for kind in ["무기", "방어구", "소모품", "전체"]:
    el_filter_btn = driver.find_element(By.CSS_SELECTOR, f'.bag-tabs button[data-filter="{kind}"]')
    el_filter_btn.click()
    # 버튼이 켜진 것을 확인하고 세야 거르기 전 칸 수를 세지 않습니다
    wait.until(lambda d, k=kind: d.find_element(
        By.CSS_SELECTOR, f'.bag-tabs button[data-filter="{k}"]').get_attribute("aria-pressed") == "true",
        message=f"{kind} 거르기 버튼이 켜지지 않음")
    filter_counts[kind] = visible_slot_count(driver)

el_table_rows = driver.find_elements(By.CSS_SELECTOR, "#inv-table tbody tr")
table_rows = len(el_table_rows)
el_inventory_count = driver.find_element(By.ID, "inventory-count")
inventory_count = el_inventory_count.text

# ── TC-5-08. 소모품 상세
select_slot(driver, wait, POTION_NAME)
detail_potion = read_detail(driver)

driver.quit()

print("고른 직후 상세:", detail_selected)
print("고른 직후 요약:", summary_selected)
print("활 장착 뒤 요약:", summary_equipped, "· 표 상태", bow_state_equipped,
      "· 보정", weapon_bonus, "· 문구", equip_msg)
print("활 + 방패 요약:", summary_both)
print("단검 교체 예고:", swap_preview, "→ 교체 뒤 요약:", summary_swapped, "· 활 상태", bow_state_swapped)
print("거르기 칸 수:", filter_counts, "· 표 행수", table_rows, "· 보유 아이템", inventory_count)
print("소모품 상세:", detail_potion)
print("머리글 골드:", header_gold_text)


# =====================================================================
# 검증 (브라우저를 닫은 뒤 모아 둔 값을 한꺼번에 비교합니다)
# =====================================================================
# TC-5-01. 4종을 산 뒤 남는 골드는 기획서 가격으로 계산합니다
assert int(header_gold_text.replace(",", "")) == EXPECTED_GOLD, \
    f"구매 뒤 머리글 골드: 기대 {EXPECTED_GOLD}, 실제 {header_gold_text!r}"

# TC-5-02. 고른 직후 상세 값을 기획서 표와 비교합니다
assert detail_selected["name"] == BOW_NAME, f"상세 이름: 기대 {BOW_NAME!r}, 실제 {detail_selected['name']!r}"
assert detail_selected["grade"] == "고급", f"상세 등급: 기대 '고급', 실제 {detail_selected['grade']!r}"
assert detail_selected["kind"] == "무기", f"상세 분류: 기대 '무기', 실제 {detail_selected['kind']!r}"
assert detail_selected["state"] == "보관 중", f"고른 직후 상태: 기대 '보관 중', 실제 {detail_selected['state']!r}"
assert detail_selected["power"] == str(BOW_POWER), \
    f"상세 전투력: 기대 {BOW_POWER}, 실제 {detail_selected['power']!r}"
assert detail_selected["change"] == f"장착 시 총 {BOW_POWER} (+{BOW_POWER})", \
    f"장착 예고: 실제 {detail_selected['change']!r}"
assert detail_selected["btn_text"] == "장착하기", f"상세 버튼 글자: 실제 {detail_selected['btn_text']!r}"

# TC-5-03. 고르기만 해서는 장착되지 않습니다
assert summary_selected == {"weapon": "없음", "armor": "없음", "power": "0"}, \
    f"고르기만 했을 때 요약: 기대 장착 없음, 실제 {summary_selected}"

# TC-5-04. 장착하면 요약 · 표 · 상세 · 보정값이 한 값으로 움직입니다
assert summary_equipped == {"weapon": BOW_NAME, "armor": "없음", "power": str(BOW_POWER)}, \
    f"활 장착 뒤 요약: 기대 {BOW_NAME}·없음·{BOW_POWER}, 실제 {summary_equipped}"
assert bow_state_equipped == "장착 중", f"활 장착 뒤 표 상태: 기대 '장착 중', 실제 {bow_state_equipped!r}"
assert detail_equipped["state"] == "장착 중", f"장착 뒤 상세 상태: 실제 {detail_equipped['state']!r}"
assert detail_equipped["btn_text"] == "장착 해제", f"장착 뒤 상세 버튼: 실제 {detail_equipped['btn_text']!r}"
assert weapon_bonus == f"+{BOW_POWER}", f"무기 보정값: 기대 '+{BOW_POWER}', 실제 {weapon_bonus!r}"
assert "filled" in weapon_slot_class, f"무기 슬롯 class: 기대 filled 포함, 실제 {weapon_slot_class!r}"
assert equip_msg == f"장착 완료: {BOW_NAME}", f"장착 결과 문구: 실제 {equip_msg!r}"

# TC-5-05. 장착 전투력은 기획서 표의 두 값을 더한 값입니다
assert summary_both == {"weapon": BOW_NAME, "armor": SHIELD_NAME, "power": str(BOW_POWER + SHIELD_POWER)}, \
    f"활 + 방패 요약: 기대 전투력 {BOW_POWER + SHIELD_POWER}, 실제 {summary_both}"

# TC-5-06. 교체 예고와 교체 결과가 같은 값이고, 이전 무기는 보관 중으로 돌아갑니다
assert swap_preview == f"장착 시 총 {DAGGER_POWER + SHIELD_POWER} ({DAGGER_POWER - BOW_POWER})", \
    f"교체 예고 문구: 실제 {swap_preview!r}"
assert summary_swapped == {"weapon": DAGGER_NAME, "armor": SHIELD_NAME,
                           "power": str(DAGGER_POWER + SHIELD_POWER)}, \
    f"교체 뒤 요약: 기대 전투력 {DAGGER_POWER + SHIELD_POWER}, 실제 {summary_swapped}"
assert bow_state_swapped == "보관 중", f"교체 뒤 활 상태: 기대 '보관 중', 실제 {bow_state_swapped!r}"

# TC-5-07. 거르기는 가방 칸만 줄이고 표는 4행 그대로입니다
assert filter_counts == FILTER_COUNTS, f"거르기 칸 수: 기대 {FILTER_COUNTS}, 실제 {filter_counts}"
assert table_rows == EXPECTED_ROWS, f"거르기 뒤 표 행수: 기대 {EXPECTED_ROWS}, 실제 {table_rows}"
assert inventory_count == str(EXPECTED_ROWS), \
    f"보유 아이템 개수: 기대 {EXPECTED_ROWS}, 실제 {inventory_count!r}"

# TC-5-08. 소모품은 장착할 수 없습니다
assert detail_potion["kind"] == "소모품", f"소모품 상세 분류: 실제 {detail_potion['kind']!r}"
assert detail_potion["btn_enabled"] is False, f"소모품 상세 버튼: 기대 비활성, 실제 {detail_potion['btn_enabled']}"
assert detail_potion["btn_text"] == "보관 중", f"소모품 버튼 글자: 실제 {detail_potion['btn_text']!r}"

# 없는 파일만 모아 개수로 판정하면 어느 스크린샷이 없는지 메시지에 남습니다
import os
missing_shots = [path for path in [shot_swapped] if not os.path.exists(path)]
assert len(missing_shots) == 0, f"스크린샷이 없습니다: {missing_shots}"

print("게임 실습 5 정답 통과")
