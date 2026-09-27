from selenium.webdriver.common.by import By

from game_login import setup, make_wait, save_screenshot, GAME_URL

START_GOLD = 1000
SPEC_ITEMS = [
    {"name": "체력 물약", "price": 50, "grade": "일반", "kind": "소모품", "power": None},
    {"name": "마나 물약", "price": 80, "grade": "일반", "kind": "소모품", "power": None},
    {"name": "강화 주문서", "price": 500, "grade": "희귀", "kind": "소모품", "power": None},
    {"name": "전설의 검", "price": 99999, "grade": "전설", "kind": "무기", "power": 500},
    {"name": "견습 단검", "price": 120, "grade": "일반", "kind": "무기", "power": 30},
    {"name": "사냥꾼의 활", "price": 260, "grade": "고급", "kind": "무기", "power": 55},
    {"name": "수호자의 방패", "price": 300, "grade": "고급", "kind": "방어구", "power": 45},
    {"name": "현자의 로브", "price": 450, "grade": "희귀", "kind": "방어구", "power": 70},
]
ROW_SELECTOR = "#shop-table tbody tr"


def to_int(text):
    return int(text.replace(",", "").replace("G", "").strip())


def count_by(rows, key):
    counts = {}
    for row in rows:
        value = row[key]
        counts.setdefault(value, 0)
        counts[value] = counts[value] + 1
    return counts


def read_shop_rows(driver):
    items = []
    el_rows = driver.find_elements(By.CSS_SELECTOR, ROW_SELECTOR)

    for el_row in el_rows:
        el_name = el_row.find_element(By.CSS_SELECTOR, "td.col-name")
        el_price = el_row.find_element(By.CSS_SELECTOR, "td.col-price")
        el_grade = el_row.find_element(By.CSS_SELECTOR, "td.col-grade")
        el_kind = el_row.find_element(By.CSS_SELECTOR, "td.col-kind")
        el_power = el_row.find_element(By.CSS_SELECTOR, "td.col-power")

        power_text = el_power.text.strip()
        if power_text == "-":
            power = None
        else:
            power = int(power_text)

        items.append({"name": el_name.text,
                      "price": to_int(el_price.text),
                      "grade": el_grade.text,
                      "kind": el_kind.text,
                      "power": power})
    return items


expected_kinds = count_by(SPEC_ITEMS, "kind")
expected_grades = count_by(SPEC_ITEMS, "grade")
expected_potion_sum = sum([item["price"] for item in SPEC_ITEMS if item["kind"] == "소모품"])
expected_affordable = [item["name"] for item in SPEC_ITEMS if item["price"] <= START_GOLD]

spec_weapons = [item for item in SPEC_ITEMS if item["kind"] == "무기"]
expected_top_weapon = max(spec_weapons, key=lambda item: item["price"])["name"]
expected_cheapest = min(SPEC_ITEMS, key=lambda item: item["price"])["name"]


driver, _ = setup()
wait = make_wait(driver, 10)

driver.get(GAME_URL + "/shop")

el_rows_right_after = driver.find_elements(By.CSS_SELECTOR, ROW_SELECTOR)
rows_right_after = len(el_rows_right_after)

wait.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, ROW_SELECTOR)) == len(SPEC_ITEMS),
           message="상점 표가 기획서 행 개수만큼 표시되지 않음")

items = read_shop_rows(driver)

el_shop_gold = driver.find_element(By.ID, "shop-gold")
screen_gold_text = el_shop_gold.text
screen_gold = to_int(screen_gold_text)

el_shop_table = driver.find_element(By.ID, "shop-table")
shot_table = save_screenshot(driver, "03_상점_표", el_shop_table)

driver.quit()


kind_counts = count_by(items, "kind")
grade_counts = count_by(items, "grade")
potion_sum = sum([item["price"] for item in items if item["kind"] == "소모품"])
affordable = [item["name"] for item in items if item["price"] <= screen_gold]

weapons = [item for item in items if item["kind"] == "무기"]
top_weapon = max(weapons, key=lambda item: item["price"])["name"]
cheapest = min(items, key=lambda item: item["price"])["name"]

print(f"연 직후 행 {rows_right_after}개 · 다 그려진 뒤 행 {len(items)}개")
print(f"분류별 {kind_counts} · 등급별 {grade_counts}")
print(f"소모품 가격 합계 {potion_sum} · 보유 골드 {screen_gold} 로 살 수 있는 아이템 {len(affordable)}종")
print(f"가장 비싼 무기 {top_weapon} · 가장 싼 아이템 {cheapest}")


assert rows_right_after == 0, f"연 직후 행: 기대 0, 실제 {rows_right_after}"
assert len(items) == len(SPEC_ITEMS), f"행 개수: 기대 {len(SPEC_ITEMS)}, 실제 {len(items)}"

assert items == SPEC_ITEMS, f"행 내용이 기획서와 다름: 기대 {SPEC_ITEMS}, 실제 {items}"

assert kind_counts == expected_kinds, f"분류별 개수: 기대 {expected_kinds}, 실제 {kind_counts}"
assert grade_counts == expected_grades, f"등급별 개수: 기대 {expected_grades}, 실제 {grade_counts}"

assert potion_sum == expected_potion_sum, \
    f"소모품 가격 합계: 기대 {expected_potion_sum}, 실제 {potion_sum}"

assert screen_gold == START_GOLD, \
    f"보유 골드: 기대 {START_GOLD}, 실제 {screen_gold} (글자 {screen_gold_text!r})"
assert len(affordable) == len(expected_affordable), \
    f"살 수 있는 아이템: 기대 {len(expected_affordable)}종 {expected_affordable}, 실제 {len(affordable)}종 {affordable}"

assert top_weapon == expected_top_weapon, f"가장 비싼 무기: 기대 {expected_top_weapon!r}, 실제 {top_weapon!r}"
assert cheapest == expected_cheapest, f"가장 싼 아이템: 기대 {expected_cheapest!r}, 실제 {cheapest!r}"

import os
missing_shots = [path for path in [shot_table] if not os.path.exists(path)]
assert len(missing_shots) == 0, f"스크린샷이 없습니다: {missing_shots}"

print("게임 실습 3 정답 통과")
