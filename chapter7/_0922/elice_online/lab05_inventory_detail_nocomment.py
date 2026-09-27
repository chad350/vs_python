from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from game_login import setup, make_wait, close_dialog, save_screenshot, GAME_URL

START_GOLD = 1000
BUY_LIST = [(1, "체력 물약", 50), (11, "견습 단검", 120), (12, "사냥꾼의 활", 260), (13, "수호자의 방패", 300)]
BOW_NAME = "사냥꾼의 활"
BOW_POWER = 55
SHIELD_NAME = "수호자의 방패"
SHIELD_POWER = 45
DAGGER_NAME = "견습 단검"
DAGGER_POWER = 30
POTION_NAME = "체력 물약"
EXPECTED_GOLD = START_GOLD - sum([item[2] for item in BUY_LIST])
EXPECTED_ROWS = len(BUY_LIST)
FILTER_COUNTS = {"무기": 2, "방어구": 1, "소모품": 1, "전체": 4}


def row_xpath(name):
    return f"//table[@id='inv-table']/tbody/tr[td[@class='col-name'][normalize-space()='{name}']]"


def row_id_of(driver, name):
    el_row = driver.find_element(By.XPATH, row_xpath(name))
    return el_row.get_attribute("data-row-id")


def table_state(driver, name):
    el_state = driver.find_element(By.XPATH, row_xpath(name) + "/td[@class='col-state']")
    return el_state.text


def select_slot(driver, wait, name):
    el_slot = driver.find_element(
        By.CSS_SELECTOR, f'#bag-grid .item-slot[data-row-id="{row_id_of(driver, name)}"]')
    el_slot.click()
    wait.until(EC.text_to_be_present_in_element((By.ID, "detail-title"), name),
               message=f"상세 패널이 {name} 으로 바뀌지 않음")


def read_detail(driver):
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
    el_weapon = driver.find_element(By.ID, "equip-weapon")
    el_armor = driver.find_element(By.ID, "equip-armor")
    el_power = driver.find_element(By.ID, "equip-power")
    return {"weapon": el_weapon.text, "armor": el_armor.text, "power": el_power.text}


def visible_slot_count(driver):
    el_slots = driver.find_elements(By.CSS_SELECTOR, "#bag-grid .item-slot")
    return len(el_slots)


driver, _ = setup()
wait = make_wait(driver, 15)

driver.get(GAME_URL + "/shop")
for item_id, name, price in BUY_LIST:
    el_buy_btn = wait.until(EC.element_to_be_clickable((By.ID, f"buy-btn-{item_id}")),
                            message=f"{name} 구매 버튼을 누를 수 없음")
    el_buy_btn.click()
    wait.until(EC.text_to_be_present_in_element((By.ID, "shop-msg"), name),
               message=f"{name} 구매 결과 문구가 나오지 않음")
    close_dialog(driver, wait)

driver.get(GAME_URL + "/inventory")
wait.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, "#inv-table tbody tr")) == EXPECTED_ROWS,
           message="인벤토리 4행이 표시되지 않음")

el_header_gold = driver.find_element(By.ID, "hdr-gold")
header_gold_text = el_header_gold.text

select_slot(driver, wait, BOW_NAME)
detail_selected = read_detail(driver)
summary_selected = read_summary(driver)

el_equip_btn = driver.find_element(By.ID, "detail-equip-btn")
el_equip_btn.click()
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

el_shield_btn = driver.find_element(By.ID, "eq-btn-" + row_id_of(driver, SHIELD_NAME))
el_shield_btn.click()
wait.until(EC.text_to_be_present_in_element((By.ID, "equip-armor"), SHIELD_NAME),
           message="방어구가 장착되지 않음")
summary_both = read_summary(driver)

select_slot(driver, wait, DAGGER_NAME)
swap_preview = read_detail(driver)["change"]

el_dagger_equip_btn = driver.find_element(By.ID, "detail-equip-btn")
el_dagger_equip_btn.click()
wait.until(EC.text_to_be_present_in_element((By.ID, "equip-weapon"), DAGGER_NAME),
           message="무기가 견습 단검으로 바뀌지 않음")

summary_swapped = read_summary(driver)
bow_state_swapped = table_state(driver, BOW_NAME)
shot_swapped = save_screenshot(driver, "05_무기_교체_뒤")

filter_counts = {}
for kind in ["무기", "방어구", "소모품", "전체"]:
    el_filter_btn = driver.find_element(By.CSS_SELECTOR, f'.bag-tabs button[data-filter="{kind}"]')
    el_filter_btn.click()
    wait.until(lambda d, k=kind: d.find_element(
        By.CSS_SELECTOR, f'.bag-tabs button[data-filter="{k}"]').get_attribute("aria-pressed") == "true",
        message=f"{kind} 거르기 버튼이 켜지지 않음")
    filter_counts[kind] = visible_slot_count(driver)

el_table_rows = driver.find_elements(By.CSS_SELECTOR, "#inv-table tbody tr")
table_rows = len(el_table_rows)
el_inventory_count = driver.find_element(By.ID, "inventory-count")
inventory_count = el_inventory_count.text

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


assert int(header_gold_text.replace(",", "")) == EXPECTED_GOLD, \
    f"구매 뒤 머리글 골드: 기대 {EXPECTED_GOLD}, 실제 {header_gold_text!r}"

assert detail_selected["name"] == BOW_NAME, f"상세 이름: 기대 {BOW_NAME!r}, 실제 {detail_selected['name']!r}"
assert detail_selected["grade"] == "고급", f"상세 등급: 기대 '고급', 실제 {detail_selected['grade']!r}"
assert detail_selected["kind"] == "무기", f"상세 분류: 기대 '무기', 실제 {detail_selected['kind']!r}"
assert detail_selected["state"] == "보관 중", f"고른 직후 상태: 기대 '보관 중', 실제 {detail_selected['state']!r}"
assert detail_selected["power"] == str(BOW_POWER), \
    f"상세 전투력: 기대 {BOW_POWER}, 실제 {detail_selected['power']!r}"
assert detail_selected["change"] == f"장착 시 총 {BOW_POWER} (+{BOW_POWER})", \
    f"장착 예고: 실제 {detail_selected['change']!r}"
assert detail_selected["btn_text"] == "장착하기", f"상세 버튼 글자: 실제 {detail_selected['btn_text']!r}"

assert summary_selected == {"weapon": "없음", "armor": "없음", "power": "0"}, \
    f"고르기만 했을 때 요약: 기대 장착 없음, 실제 {summary_selected}"

assert summary_equipped == {"weapon": BOW_NAME, "armor": "없음", "power": str(BOW_POWER)}, \
    f"활 장착 뒤 요약: 기대 {BOW_NAME}·없음·{BOW_POWER}, 실제 {summary_equipped}"
assert bow_state_equipped == "장착 중", f"활 장착 뒤 표 상태: 기대 '장착 중', 실제 {bow_state_equipped!r}"
assert detail_equipped["state"] == "장착 중", f"장착 뒤 상세 상태: 실제 {detail_equipped['state']!r}"
assert detail_equipped["btn_text"] == "장착 해제", f"장착 뒤 상세 버튼: 실제 {detail_equipped['btn_text']!r}"
assert weapon_bonus == f"+{BOW_POWER}", f"무기 보정값: 기대 '+{BOW_POWER}', 실제 {weapon_bonus!r}"
assert "filled" in weapon_slot_class, f"무기 슬롯 class: 기대 filled 포함, 실제 {weapon_slot_class!r}"
assert equip_msg == f"장착 완료: {BOW_NAME}", f"장착 결과 문구: 실제 {equip_msg!r}"

assert summary_both == {"weapon": BOW_NAME, "armor": SHIELD_NAME, "power": str(BOW_POWER + SHIELD_POWER)}, \
    f"활 + 방패 요약: 기대 전투력 {BOW_POWER + SHIELD_POWER}, 실제 {summary_both}"

assert swap_preview == f"장착 시 총 {DAGGER_POWER + SHIELD_POWER} ({DAGGER_POWER - BOW_POWER})", \
    f"교체 예고 문구: 실제 {swap_preview!r}"
assert summary_swapped == {"weapon": DAGGER_NAME, "armor": SHIELD_NAME,
                           "power": str(DAGGER_POWER + SHIELD_POWER)}, \
    f"교체 뒤 요약: 기대 전투력 {DAGGER_POWER + SHIELD_POWER}, 실제 {summary_swapped}"
assert bow_state_swapped == "보관 중", f"교체 뒤 활 상태: 기대 '보관 중', 실제 {bow_state_swapped!r}"

assert filter_counts == FILTER_COUNTS, f"거르기 칸 수: 기대 {FILTER_COUNTS}, 실제 {filter_counts}"
assert table_rows == EXPECTED_ROWS, f"거르기 뒤 표 행수: 기대 {EXPECTED_ROWS}, 실제 {table_rows}"
assert inventory_count == str(EXPECTED_ROWS), \
    f"보유 아이템 개수: 기대 {EXPECTED_ROWS}, 실제 {inventory_count!r}"

assert detail_potion["kind"] == "소모품", f"소모품 상세 분류: 실제 {detail_potion['kind']!r}"
assert detail_potion["btn_enabled"] is False, f"소모품 상세 버튼: 기대 비활성, 실제 {detail_potion['btn_enabled']}"
assert detail_potion["btn_text"] == "보관 중", f"소모품 버튼 글자: 실제 {detail_potion['btn_text']!r}"

import os
missing_shots = [path for path in [shot_swapped] if not os.path.exists(path)]
assert len(missing_shots) == 0, f"스크린샷이 없습니다: {missing_shots}"

print("게임 실습 5 정답 통과")
