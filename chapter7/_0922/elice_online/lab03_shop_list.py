"""실습 3. 상점 목록 수집·정제·기획서 대조 · 정답 코드와 해설

화면 /shop        테스트 케이스 7개 (TC-3-01 ~ TC-3-07)

이 실습이 확인하는 것은 3가지입니다.
  ① 0.5초 뒤에 오는 상점 목록을 행 개수 조건으로 기다리는가
  ② 행 하나를 딕셔너리 하나로 모아 기획서 표와 값·차례까지 같은가
  ③ 합계·개수·최고가·최저가 같은 기대값을 화면이 아니라 기획서 표에서 계산하는가

읽은 값은 읽는 즉시 판단하지 않고 변수에 모아 두고, 브라우저를 닫은 뒤 마지막에 한꺼번에 비교합니다.
중간에 assert 로 멈추면 남은 값을 확인하지 못하고 스크린샷도 남지 않기 때문입니다.
"""
from selenium.webdriver.common.by import By

from game_login import setup, make_wait, save_screenshot, GAME_URL

# ── 기획 데이터 (화면에서 읽지 않고 기획서 값을 코드에 적습니다)
# 화면이 이 값과 다르면 기대값을 고치지 않고 「다르다」 고 보고합니다.
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
    """'1,200 G' 처럼 쉼표와 단위가 든 글자를 정수로 바꿉니다.

    화면에서 얻은 데이터는 문자열로 저장됩니다.
    쉼표와 G 가 남아 있으면 int() 가 ValueError 를 내므로 먼저 지운 뒤 양쪽 공백을 없앱니다.
    """
    return int(text.replace(",", "").replace("G", "").strip())


def count_by(rows, key):
    """딕셔너리 목록을 key 값별로 세어 {값: 개수} 딕셔너리를 만듭니다.

    화면에서 모은 목록과 기획서 목록에 같은 함수를 사용합니다.
    같은 방법으로 세어야 두 결과를 그대로 비교할 수 있습니다.
    """
    counts = {}
    for row in rows:
        value = row[key]
        counts.setdefault(value, 0)
        counts[value] = counts[value] + 1
    return counts


def read_shop_rows(driver):
    """상점 표의 행을 딕셔너리 목록으로 모읍니다 (TC-3-03)."""
    items = []
    el_rows = driver.find_elements(By.CSS_SELECTOR, ROW_SELECTOR)

    for el_row in el_rows:
        # 열마다 목록을 따로 만들면 이름과 가격의 순번이 달라져도 알아채지 못합니다.
        # 행 1개를 딕셔너리 1개로 만들면 같은 행의 값이 언제나 한 묶음으로 남습니다
        el_name = el_row.find_element(By.CSS_SELECTOR, "td.col-name")
        el_price = el_row.find_element(By.CSS_SELECTOR, "td.col-price")
        el_grade = el_row.find_element(By.CSS_SELECTOR, "td.col-grade")
        el_kind = el_row.find_element(By.CSS_SELECTOR, "td.col-kind")
        el_power = el_row.find_element(By.CSS_SELECTOR, "td.col-power")

        power_text = el_power.text.strip()
        # 소모품은 전투력 칸이 - 입니다.
        # 그대로 int() 에 넣으면 ValueError 가 발생합니다
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


# =====================================================================
# 기대값 계산 (화면을 열기 전에 기획서 표로 먼저 계산합니다)
# =====================================================================
# 화면에서 모은 값으로 기대값을 만들면, 화면이 틀려도 합계가 맞아 버려서 확인이 되지 않습니다.
expected_kinds = count_by(SPEC_ITEMS, "kind")
expected_grades = count_by(SPEC_ITEMS, "grade")
# sum 에 대괄호를 넣어 「목록을 먼저 만든 뒤 합계를 구한다」 2단계가 코드에 보이게 합니다.
# 대괄호가 없으면 중간 목록이 남지 않아, 합계가 다를 때 어떤 가격이 들어갔는지 확인하기 어렵습니다
expected_potion_sum = sum([item["price"] for item in SPEC_ITEMS if item["kind"] == "소모품"])
expected_affordable = [item["name"] for item in SPEC_ITEMS if item["price"] <= START_GOLD]

# max 와 min 은 기본적으로 값 자체를 비교합니다.
# 딕셔너리는 크기를 비교할 수 없어 TypeError 가 발생합니다.
# key 에 lambda 를 지정하면 「무엇을 기준으로 비교할지」 만 알려 주고, 반환값은 딕셔너리 그대로 유지됩니다
spec_weapons = [item for item in SPEC_ITEMS if item["kind"] == "무기"]
expected_top_weapon = max(spec_weapons, key=lambda item: item["price"])["name"]
expected_cheapest = min(SPEC_ITEMS, key=lambda item: item["price"])["name"]


# =====================================================================
# 진행
# =====================================================================
driver, _ = setup()
# 상점 목록은 0.5초 뒤에 오므로 기다리는 시간을 10초로 정한 Wait 를 따로 만듭니다
wait = make_wait(driver, 10)

driver.get(GAME_URL + "/shop")

# ── TC-3-01. 화면을 연 직후의 행 개수
# 목록 응답이 오기 전이라 0개입니다.
# 이 값을 확인해 두어야 「기다림이 필요하다」 는 근거가 남습니다
el_rows_right_after = driver.find_elements(By.CSS_SELECTOR, ROW_SELECTOR)
rows_right_after = len(el_rows_right_after)

# ── TC-3-02. 행 개수가 기획서 8행이 될 때까지 기다리기
# 요소 1개가 나타나는 것을 조건으로 두면 표를 반만 만든 상태에서도 통과합니다.
# 개수를 조건으로 두면 마지막 행까지 만든 뒤에 읽습니다
# wait.until 은 조건을 일정 간격으로 다시 실행하므로 함수를 전달해야 합니다.
# lambda 는 이름 없는 함수라, d(그때의 driver)로 행을 다시 세는 조건을 def 없이 작성할 수 있습니다
wait.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, ROW_SELECTOR)) == len(SPEC_ITEMS),
           message="상점 표가 기획서 행 개수만큼 표시되지 않음")

# ── TC-3-03. 행 8개를 딕셔너리 목록으로 수집
items = read_shop_rows(driver)

# ── TC-3-06. 보유 골드
# 원본 글자도 함께 보관합니다.
# 값이 다를 때 실패 메시지에 화면 표기를 그대로 남기기 위해서입니다
el_shop_gold = driver.find_element(By.ID, "shop-gold")
screen_gold_text = el_shop_gold.text
screen_gold = to_int(screen_gold_text)

# ── 스크린샷 (값을 모두 읽은 뒤, 브라우저를 닫기 전에 남깁니다)
el_shop_table = driver.find_element(By.ID, "shop-table")
shot_table = save_screenshot(driver, "03_상점_표", el_shop_table)

driver.quit()


# =====================================================================
# 화면에서 모은 값으로 같은 계산을 합니다 (기대값과 같은 방법을 사용합니다)
# =====================================================================
# ── TC-3-04. 분류별 · 등급별 개수
kind_counts = count_by(items, "kind")
grade_counts = count_by(items, "grade")
# ── TC-3-05. 소모품 가격 합계
potion_sum = sum([item["price"] for item in items if item["kind"] == "소모품"])
affordable = [item["name"] for item in items if item["price"] <= screen_gold]

# ── TC-3-07. 가장 비싼 무기와 가장 싼 아이템
# 기대값을 만들 때와 같은 방법으로 계산합니다.
# key=lambda 로 비교 기준을 가격으로 지정합니다
weapons = [item for item in items if item["kind"] == "무기"]
top_weapon = max(weapons, key=lambda item: item["price"])["name"]
cheapest = min(items, key=lambda item: item["price"])["name"]

print(f"연 직후 행 {rows_right_after}개 · 다 그려진 뒤 행 {len(items)}개")
print(f"분류별 {kind_counts} · 등급별 {grade_counts}")
print(f"소모품 가격 합계 {potion_sum} · 보유 골드 {screen_gold} 로 살 수 있는 아이템 {len(affordable)}종")
print(f"가장 비싼 무기 {top_weapon} · 가장 싼 아이템 {cheapest}")


# =====================================================================
# 검증 (브라우저를 닫은 뒤 모아 둔 값을 한꺼번에 비교합니다)
# =====================================================================
# TC-3-01 · TC-3-02. 연 직후에는 0행, 기다린 뒤에는 기획서와 같은 8행입니다
assert rows_right_after == 0, f"연 직후 행: 기대 0, 실제 {rows_right_after}"
assert len(items) == len(SPEC_ITEMS), f"행 개수: 기대 {len(SPEC_ITEMS)}, 실제 {len(items)}"

# TC-3-03. 값과 차례까지 같은지 목록 전체를 한 번에 비교합니다.
# 이름만 비교하면 가격·등급이 어긋난 것을 지나칩니다
assert items == SPEC_ITEMS, f"행 내용이 기획서와 다름: 기대 {SPEC_ITEMS}, 실제 {items}"

# TC-3-04. 분류별·등급별 개수
assert kind_counts == expected_kinds, f"분류별 개수: 기대 {expected_kinds}, 실제 {kind_counts}"
assert grade_counts == expected_grades, f"등급별 개수: 기대 {expected_grades}, 실제 {grade_counts}"

# TC-3-05. 소모품 가격 합계
assert potion_sum == expected_potion_sum, \
    f"소모품 가격 합계: 기대 {expected_potion_sum}, 실제 {potion_sum}"

# TC-3-06. 보유 골드와 살 수 있는 아이템 개수
assert screen_gold == START_GOLD, \
    f"보유 골드: 기대 {START_GOLD}, 실제 {screen_gold} (글자 {screen_gold_text!r})"
assert len(affordable) == len(expected_affordable), \
    f"살 수 있는 아이템: 기대 {len(expected_affordable)}종 {expected_affordable}, 실제 {len(affordable)}종 {affordable}"

# TC-3-07. 가장 비싼 무기와 가장 싼 아이템
assert top_weapon == expected_top_weapon, f"가장 비싼 무기: 기대 {expected_top_weapon!r}, 실제 {top_weapon!r}"
assert cheapest == expected_cheapest, f"가장 싼 아이템: 기대 {expected_cheapest!r}, 실제 {cheapest!r}"

# 스크린샷이 실제로 저장되었는지 확인합니다 (save_screenshot 이 파일 경로를 반환합니다)
import os
# 없는 파일만 모아 개수로 판정하면 어느 스크린샷이 없는지 메시지에 남습니다
missing_shots = [path for path in [shot_table] if not os.path.exists(path)]
assert len(missing_shots) == 0, f"스크린샷이 없습니다: {missing_shots}"

print("게임 실습 3 정답 통과")
