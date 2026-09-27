from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from game_login import setup, make_wait, save_screenshot, GAME_URL

SPEC_LOTS = [{"lot": "A-01", "name": "새벽 물약", "grade": "일반", "price": 1200, "date": "2026-09-01"},
             {"lot": "A-02", "name": "달빛 물약", "grade": "일반", "price": 2500, "date": "2026-09-01"},
             {"lot": "A-03", "name": "은하 물약", "grade": "고급", "price": 5000, "date": "2026-09-02"},
             {"lot": "A-04", "name": "서리 물약", "grade": "고급", "price": 7400, "date": "2026-09-02"},
             {"lot": "A-05", "name": "용암 물약", "grade": "희귀", "price": 12000, "date": "2026-09-03"},
             {"lot": "A-06", "name": "별빛 단검", "grade": "일반", "price": 900, "date": "2026-09-03"},
             {"lot": "A-07", "name": "달빛검", "grade": "고급", "price": 4800, "date": "2026-09-04"},
             {"lot": "A-08", "name": "서리검", "grade": "고급", "price": 6200, "date": "2026-09-04"},
             {"lot": "A-09", "name": "용암검", "grade": "희귀", "price": 15500, "date": "2026-09-05"},
             {"lot": "A-10", "name": "새벽 방패", "grade": "일반", "price": 1600, "date": "2026-09-05"},
             {"lot": "A-11", "name": "달빛 방패", "grade": "고급", "price": 5600, "date": "2026-09-06"},
             {"lot": "A-12", "name": "서리 방패", "grade": "희귀", "price": 9800, "date": "2026-09-06"},
             {"lot": "A-13", "name": "별빛 로브", "grade": "고급", "price": 4300, "date": "2026-09-07"},
             {"lot": "A-14", "name": "달빛 로브", "grade": "희귀", "price": 11200, "date": "2026-09-07"},
             {"lot": "A-15", "name": "은하 로브", "grade": "전설", "price": 32000, "date": "2026-09-08"},
             {"lot": "A-16", "name": "새벽 반지", "grade": "일반", "price": 800, "date": "2026-09-08"},
             {"lot": "A-17", "name": "달빛 반지", "grade": "고급", "price": 3900, "date": "2026-09-09"},
             {"lot": "A-18", "name": "은하 반지", "grade": "희귀", "price": 10400, "date": "2026-09-09"},
             {"lot": "A-19", "name": "별빛 부적", "grade": "일반", "price": 2100, "date": "2026-09-10"},
             {"lot": "A-20", "name": "서리 부적", "grade": "고급", "price": 6900, "date": "2026-09-10"},
             {"lot": "A-21", "name": "용암 부적", "grade": "희귀", "price": 13800, "date": "2026-09-11"},
             {"lot": "A-22", "name": "새벽 깃발", "grade": "일반", "price": 1400, "date": "2026-09-11"},
             {"lot": "A-23", "name": "달빛 깃발", "grade": "고급", "price": 5200, "date": "2026-09-12"},
             {"lot": "A-24", "name": "은하 깃발", "grade": "전설", "price": 28800, "date": "2026-09-12"}]

SEARCHING_TEXT = "검색 중..."
DEFAULT_MIN = "0"
DEFAULT_MAX = "50000"
DEFAULT_FROM = "2026-09-01"
DEFAULT_TO = "2026-09-12"
NEW_TO = "2026-09-03"
POTION_KEYWORD = "물약"
POTION_MAX = 5000
LEGEND_GRADE = "전설"


def step(title):
    print(f"\n=== {title} ===")


def lots_of(rows):
    return [row["lot"] for row in rows]


def name_match(rows, keyword, max_price):
    return [row for row in rows if keyword in row["name"] and row["price"] <= max_price]


def card_lot_numbers(driver):
    lot_numbers = []
    el_cards = driver.find_elements(By.CSS_SELECTOR, "#auc-list .auc-card")

    for el_card in el_cards:
        card_id = el_card.get_attribute("id")
        lot_numbers.append(card_id.removeprefix("auc-card-"))
    return lot_numbers


def count_of(text):
    return int(text.replace("검색 결과", "").replace("건", "").strip())


def set_text(driver, element_id, value):
    el_input = driver.find_element(By.ID, element_id)
    el_input.clear()
    el_input.send_keys(value)


def run_search(driver, wait, before_cards):
    el_search_btn = driver.find_element(By.ID, "auc-search")
    el_search_btn.click()

    wait.until(EC.text_to_be_present_in_element((By.ID, "auc-count"), SEARCHING_TEXT),
               message="건수 문구가 검색 중... 이 되지 않음")
    right_after = card_lot_numbers(driver)

    wait.until(lambda d: d.find_element(By.ID, "auc-count").text.startswith("검색 결과"),
               message="1.5초 뒤 검색 결과 건수 문구가 나오지 않음")

    el_count = driver.find_element(By.ID, "auc-count")
    return {"count": count_of(el_count.text),
            "cards": card_lot_numbers(driver),
            "right_after": right_after,
            "before": before_cards}


def report(result, expected_lots):
    print(f" 검색 결과 {result['count']}건 · 카드 {result['cards']}"
          f" · 누른 직후 남아 있던 카드 {result['right_after']} (앞 검색 결과 {result['before']})")
    print(f" 기획서 기대 {len(expected_lots)}건 {expected_lots}"
          f" · 화면 실제 {result['count']}건 {result['cards']}")

    missing = [lot for lot in expected_lots if lot not in result["cards"]]
    extra = [lot for lot in result["cards"] if lot not in expected_lots]

    if len(missing) > 0 or len(extra) > 0:
        print(f" 빠진 매물 {missing} · 더 들어온 매물 {extra}")
    return missing, extra


driver, _ = setup()
wait = make_wait(driver, 10)

driver.get(GAME_URL + "/auction")
wait.until(EC.element_to_be_clickable((By.ID, "auc-search")),
           message="경매장 검색 화면이 열리지 않음")

step(f"검색 1 · 이름 {POTION_KEYWORD} · 가격 0~{POTION_MAX}")
expected_potion = lots_of(name_match(SPEC_LOTS, POTION_KEYWORD, POTION_MAX))
set_text(driver, "auc-name", POTION_KEYWORD)
set_text(driver, "auc-min", DEFAULT_MIN)
set_text(driver, "auc-max", str(POTION_MAX))

result_potion = run_search(driver, wait, [])
el_auc_list = driver.find_element(By.ID, "auc-list")
shot_potion = save_screenshot(driver, f"07_물약_0-{POTION_MAX}_결과", el_auc_list)
missing_potion, extra_potion = report(result_potion, expected_potion)

step(f"검색 2 · 등급 {LEGEND_GRADE}")
expected_legend = lots_of([row for row in SPEC_LOTS if row["grade"] == LEGEND_GRADE])
el_name = driver.find_element(By.ID, "auc-name")
el_name.clear()
el_grade = driver.find_element(By.ID, "auc-grade")
Select(el_grade).select_by_value(LEGEND_GRADE)
set_text(driver, "auc-min", DEFAULT_MIN)
set_text(driver, "auc-max", DEFAULT_MAX)

result_legend = run_search(driver, wait, result_potion["cards"])
report(result_legend, expected_legend)

step(f"검색 3 · 기간 {DEFAULT_FROM} ~ {NEW_TO}")
el_to = driver.find_element(By.ID, "auc-to")
readonly_attr = el_to.get_attribute("readonly")
value_before_keys = el_to.get_attribute("value")
el_to.send_keys(NEW_TO)
value_after_keys = el_to.get_attribute("value")
print(f" auc-to readonly 속성 {readonly_attr!r}"
      f" · send_keys 전 {value_before_keys!r} · send_keys 뒤 {value_after_keys!r}")

driver.execute_script(
    "const el = document.getElementById('auc-to');"
    "el.value = arguments[0];"
    "el.dispatchEvent(new Event('input', {bubbles: true}));"
    "el.dispatchEvent(new Event('change', {bubbles: true}));", NEW_TO)

el_to = driver.find_element(By.ID, "auc-to")
el_from = driver.find_element(By.ID, "auc-from")
value_after_js = el_to.get_attribute("value")
value_from = el_from.get_attribute("value")
print(f" JS 로 넣은 뒤 auc-to {value_after_js!r} · auc-from {value_from!r}")

expected_period = lots_of([row for row in SPEC_LOTS
                           if DEFAULT_FROM <= row["date"] <= NEW_TO])
el_grade = driver.find_element(By.ID, "auc-grade")
Select(el_grade).select_by_value("전체")
result_period = run_search(driver, wait, result_legend["cards"])
report(result_period, expected_period)

el_empty = driver.find_element(By.ID, "auc-empty")
empty_shown = el_empty.is_displayed()

driver.quit()


assert result_legend["right_after"] == result_legend["before"] and result_legend["before"] != [], \
    (f"찾기를 누른 직후 카드: 기대 앞 검색 결과 {result_legend['before']} 그대로, "
     f"실제 {result_legend['right_after']}")

assert value_after_keys == value_before_keys == DEFAULT_TO, \
    (f"readonly 칸 send_keys: 기대 값이 그대로 {DEFAULT_TO!r}, "
     f"실제 {value_before_keys!r} → {value_after_keys!r}")

assert value_after_js == NEW_TO, f"JS 로 넣은 auc-to 값: 기대 {NEW_TO!r}, 실제 {value_after_js!r}"
assert value_from == DEFAULT_FROM, f"auc-from 기본값: 기대 {DEFAULT_FROM!r}, 실제 {value_from!r}"

assert result_legend["cards"] == expected_legend and result_legend["count"] == len(expected_legend), \
    (f"등급 {LEGEND_GRADE!r}: 기대 {len(expected_legend)}건 {expected_legend}, "
     f"실제 {result_legend['count']}건 {result_legend['cards']}")

assert result_period["cards"] == expected_period and result_period["count"] == len(expected_period), \
    (f"기간 {DEFAULT_FROM}~{NEW_TO}: 기대 {len(expected_period)}건 {expected_period}, "
     f"실제 {result_period['count']}건 {result_period['cards']}")

assert empty_shown is False, "결과가 있는데 빈 결과 안내가 보입니다"

import os
missing_shots = [path for path in [shot_potion] if not os.path.exists(path)]
assert len(missing_shots) == 0, f"스크린샷이 없습니다: {missing_shots}"

assert result_potion["cards"] == expected_potion and result_potion["count"] == len(expected_potion), \
    (f"이름 {POTION_KEYWORD!r} · 가격 0~{POTION_MAX}: "
     f"기대 {len(expected_potion)}건 {expected_potion}, "
     f"실제 {result_potion['count']}건 {result_potion['cards']}. "
     f"빠진 매물 {missing_potion} · 더 들어온 매물 {extra_potion}. "
     f"가격이 최대값 {POTION_MAX} 과 정확히 같은 A-03(5,000)이 빠집니다 (기획서는 최대 이하)")
