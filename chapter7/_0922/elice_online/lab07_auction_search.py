"""실습 7. 경매장 검색 조건 조합과 경계값 · 정답 코드와 해설

화면 /auction        테스트 케이스 7개 (TC-7-01 ~ TC-7-07)

이 실습이 확인하는 것은 3가지입니다.
  ① 1.5초 동안 남아 있는 앞 검색 결과를 새 결과로 읽지 않는가
  ② readonly 칸에 send_keys 가 예외 없이 지나간 뒤 값을 다시 읽어 확인하는가
  ③ 가격 최대값과 정확히 같은 매물이 결과에 들어오는지 경계값으로 확인하는가

이 문항은 AssertionError 로 끝나는 것이 정답입니다 (종료 코드 1).
기획서와 다른 값이 나와도 조건을 고쳐 통과시키지 않고, 빠진 매물과 더 들어온 매물을 세어 보고합니다.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from game_login import setup, make_wait, save_screenshot, GAME_URL

# ── 기획 데이터 (화면에서 읽지 않고 기획서 매물 24건을 코드에 적습니다)
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
    """진행 단계를 출력합니다.

    어느 단계의 값인지 출력에서 구분하기 위해서입니다.
    """
    print(f"\n=== {title} ===")


def lots_of(rows):
    """기획서 행 목록에서 매물 번호만 뽑습니다."""
    return [row["lot"] for row in rows]


def name_match(rows, keyword, max_price):
    """이름과 가격 조건으로 기대 매물을 계산합니다 (TC-7-01).

    기획서의 가격 최대는 「이하」 이므로 최대값과 정확히 같은 매물도 넣습니다.
    이 경계를 화면 값으로 맞추면 확인하려던 것이 없어집니다.
    """
    return [row for row in rows if keyword in row["name"] and row["price"] <= max_price]


def card_lot_numbers(driver):
    """지금 화면에 있는 결과 카드의 매물 번호 목록을 만듭니다."""
    lot_numbers = []
    el_cards = driver.find_elements(By.CSS_SELECTOR, "#auc-list .auc-card")

    for el_card in el_cards:
        # 카드 id 는 auc-card-A-07 모양이라 앞부분을 떼어 매물 번호만 남깁니다
        card_id = el_card.get_attribute("id")
        lot_numbers.append(card_id.removeprefix("auc-card-"))
    return lot_numbers


def count_of(text):
    """건수 문구에서 숫자만 뽑아 정수로 바꿉니다.

    「검색 결과 6건」 을 그대로 int() 에 넣으면 ValueError 가 발생합니다.
    앞뒤 글자를 지운 뒤 숫자만 남겨 바꿉니다.
    """
    return int(text.replace("검색 결과", "").replace("건", "").strip())


def set_text(driver, element_id, value):
    """입력 칸의 값을 지우고 새 값을 넣습니다.

    지우지 않고 넣으면 앞 검색어 뒤에 붙어 조건이 달라집니다.
    """
    el_input = driver.find_element(By.ID, element_id)
    el_input.clear()
    el_input.send_keys(value)


def run_search(driver, wait, before_cards):
    """찾기를 누르고 결과를 기다린 뒤 건수 · 카드 · 누른 직후 카드를 모읍니다.

    앞 검색의 결과 카드는 1.5초 동안 그대로 남아 있습니다.
    카드가 아니라 건수 문구가 채워지는 것을 조건으로 써야 새 결과를 읽습니다.
    """
    el_search_btn = driver.find_element(By.ID, "auc-search")
    el_search_btn.click()

    # 먼저 「검색 중...」 이 되는 것을 확인해야, 누른 것이 화면에 반영되었다는 근거가 남습니다
    wait.until(EC.text_to_be_present_in_element((By.ID, "auc-count"), SEARCHING_TEXT),
               message="건수 문구가 검색 중... 이 되지 않음")
    # TC-7-02. 이 시점의 카드를 읽어 두면 앞 검색 결과가 남아 있다는 증거가 됩니다
    right_after = card_lot_numbers(driver)

    # wait.until 은 조건을 0.5초 간격으로 다시 실행해 참이 될 때까지 기다립니다.
    # 그래서 인자로 「값」 이 아니라 「호출할 함수」 를 전달해야 합니다.
    #   d.find_element(...).text.startswith(...)      ← 지금 시점에서 한 번 계산한 True/False 입니다
    #   lambda d: d.find_element(...).text.startswith(...)  ← 회차마다 다시 계산하는 함수입니다
    # lambda 는 이름 없는 함수라 def 로 따로 정의하지 않고 조건 1개를 그대로 작성할 수 있고,
    # 매개변수 d 에는 wait 를 만들 때 지정한 driver 가 회차마다 전달됩니다
    wait.until(lambda d: d.find_element(By.ID, "auc-count").text.startswith("검색 결과"),
               message="1.5초 뒤 검색 결과 건수 문구가 나오지 않음")

    el_count = driver.find_element(By.ID, "auc-count")
    return {"count": count_of(el_count.text),
            "cards": card_lot_numbers(driver),
            "right_after": right_after,
            "before": before_cards}


def report(result, expected_lots):
    """검색 1건의 결과를 기획서 기대와 나란히 출력합니다.

    빠진 매물과 더 들어온 매물을 각각 세어 두면 어느 방향으로 다른지 알 수 있습니다.
    """
    print(f" 검색 결과 {result['count']}건 · 카드 {result['cards']}"
          f" · 누른 직후 남아 있던 카드 {result['right_after']} (앞 검색 결과 {result['before']})")
    print(f" 기획서 기대 {len(expected_lots)}건 {expected_lots}"
          f" · 화면 실제 {result['count']}건 {result['cards']}")

    # 기대에는 있는데 화면에 없는 것과, 화면에만 있는 것을 따로 모읍니다
    missing = [lot for lot in expected_lots if lot not in result["cards"]]
    extra = [lot for lot in result["cards"] if lot not in expected_lots]

    if len(missing) > 0 or len(extra) > 0:
        print(f" 빠진 매물 {missing} · 더 들어온 매물 {extra}")
    return missing, extra


# =====================================================================
# 진행
# =====================================================================
driver, _ = setup()
wait = make_wait(driver, 10)

driver.get(GAME_URL + "/auction")
# 화면이 준비되기 전에 조건 칸을 찾으면 NoSuchElementException 이 발생합니다
wait.until(EC.element_to_be_clickable((By.ID, "auc-search")),
           message="경매장 검색 화면이 열리지 않음")

# ── TC-7-01 · TC-7-02. 이름과 가격 경계값
step(f"검색 1 · 이름 {POTION_KEYWORD} · 가격 0~{POTION_MAX}")
expected_potion = lots_of(name_match(SPEC_LOTS, POTION_KEYWORD, POTION_MAX))
set_text(driver, "auc-name", POTION_KEYWORD)
set_text(driver, "auc-min", DEFAULT_MIN)
set_text(driver, "auc-max", str(POTION_MAX))

result_potion = run_search(driver, wait, [])
el_auc_list = driver.find_element(By.ID, "auc-list")
shot_potion = save_screenshot(driver, f"07_물약_0-{POTION_MAX}_결과", el_auc_list)
missing_potion, extra_potion = report(result_potion, expected_potion)

# ── TC-7-03. 등급 조건
step(f"검색 2 · 등급 {LEGEND_GRADE}")
expected_legend = lots_of([row for row in SPEC_LOTS if row["grade"] == LEGEND_GRADE])
el_name = driver.find_element(By.ID, "auc-name")
el_name.clear()
el_grade = driver.find_element(By.ID, "auc-grade")
# select 는 click 과 send_keys 로 다루면 브라우저마다 다르게 움직입니다.
# Select 로 값을 지정하면 change 가 함께 일어납니다
Select(el_grade).select_by_value(LEGEND_GRADE)
set_text(driver, "auc-min", DEFAULT_MIN)
set_text(driver, "auc-max", DEFAULT_MAX)

result_legend = run_search(driver, wait, result_potion["cards"])
report(result_legend, expected_legend)

# ── TC-7-04 · TC-7-05 · TC-7-06. 기간 칸과 readonly
step(f"검색 3 · 기간 {DEFAULT_FROM} ~ {NEW_TO}")
el_to = driver.find_element(By.ID, "auc-to")
readonly_attr = el_to.get_attribute("readonly")
value_before_keys = el_to.get_attribute("value")
# readonly 칸에 send_keys 를 하면 예외 없이 지나갑니다.
# 값이 들어갔다고 여기기 쉬우므로 넣은 뒤 value 를 다시 읽어 확인합니다
el_to.send_keys(NEW_TO)
value_after_keys = el_to.get_attribute("value")
print(f" auc-to readonly 속성 {readonly_attr!r}"
      f" · send_keys 전 {value_before_keys!r} · send_keys 뒤 {value_after_keys!r}")

# JS 로 value 만 바꾸면 화면은 값이 바뀐 것을 알아차리지 못합니다.
# 화면이 듣고 있는 input 과 change 이벤트를 같이 보내야 새 조건으로 검색합니다
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

# ── TC-7-07. 결과가 있을 때 빈 결과 안내
el_empty = driver.find_element(By.ID, "auc-empty")
empty_shown = el_empty.is_displayed()

driver.quit()


# =====================================================================
# 검증 (브라우저를 닫은 뒤 모아 둔 값을 한꺼번에 비교합니다)
# =====================================================================
# TC-7-02. 찾기를 누른 직후 카드는 앞 검색 결과 그대로입니다.
# 검색 2에서 확인합니다.
# 검색 1은 앞 검색이 없어 빈 목록이기 때문입니다
assert result_legend["right_after"] == result_legend["before"] and result_legend["before"] != [], \
    (f"찾기를 누른 직후 카드: 기대 앞 검색 결과 {result_legend['before']} 그대로, "
     f"실제 {result_legend['right_after']}")

# TC-7-04. readonly 칸은 send_keys 앞뒤로 값이 같습니다
assert value_after_keys == value_before_keys == DEFAULT_TO, \
    (f"readonly 칸 send_keys: 기대 값이 그대로 {DEFAULT_TO!r}, "
     f"실제 {value_before_keys!r} → {value_after_keys!r}")

# TC-7-05. JS 로 값을 넣고 이벤트를 보내면 값이 바뀝니다
assert value_after_js == NEW_TO, f"JS 로 넣은 auc-to 값: 기대 {NEW_TO!r}, 실제 {value_after_js!r}"
assert value_from == DEFAULT_FROM, f"auc-from 기본값: 기대 {DEFAULT_FROM!r}, 실제 {value_from!r}"

# TC-7-03. 등급 조건은 기획서 계산값과 같습니다
assert result_legend["cards"] == expected_legend and result_legend["count"] == len(expected_legend), \
    (f"등급 {LEGEND_GRADE!r}: 기대 {len(expected_legend)}건 {expected_legend}, "
     f"실제 {result_legend['count']}건 {result_legend['cards']}")

# TC-7-06. 기간 조건도 기획서 계산값과 같습니다
assert result_period["cards"] == expected_period and result_period["count"] == len(expected_period), \
    (f"기간 {DEFAULT_FROM}~{NEW_TO}: 기대 {len(expected_period)}건 {expected_period}, "
     f"실제 {result_period['count']}건 {result_period['cards']}")

# TC-7-07. 결과가 있으므로 빈 결과 안내는 보이지 않습니다
assert empty_shown is False, "결과가 있는데 빈 결과 안내가 보입니다"

# 없는 파일만 모아 개수로 판정하면 어느 스크린샷이 없는지 메시지에 남습니다
import os
missing_shots = [path for path in [shot_potion] if not os.path.exists(path)]
assert len(missing_shots) == 0, f"스크린샷이 없습니다: {missing_shots}"

# TC-7-01. 가격 경계값 비교를 마지막에 두어, 다른 조건을 모두 확인한 뒤 보고합니다.
# 기대 목록을 화면 값으로 고치면 경계값을 확인하려던 이 문항의 목적이 없어집니다
assert result_potion["cards"] == expected_potion and result_potion["count"] == len(expected_potion), \
    (f"이름 {POTION_KEYWORD!r} · 가격 0~{POTION_MAX}: "
     f"기대 {len(expected_potion)}건 {expected_potion}, "
     f"실제 {result_potion['count']}건 {result_potion['cards']}. "
     f"빠진 매물 {missing_potion} · 더 들어온 매물 {extra_potion}. "
     f"가격이 최대값 {POTION_MAX} 과 정확히 같은 A-03(5,000)이 빠집니다 (기획서는 최대 이하)")
