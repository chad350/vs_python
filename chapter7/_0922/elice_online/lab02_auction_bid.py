"""실습 2. 경매장 입찰 상태 추적과 기록 대조 · 정답 코드와 해설

화면 /auction        테스트 케이스 8개 (TC-2-01 ~ TC-2-08)

이 실습이 확인하는 것은 3가지입니다.
  ① 1.5초 뒤에 오는 검색 결과를 건수 문구 조건으로 기다리는가
  ② 입찰 상태가 접수에서 확정으로 바뀌는 3초를 초 세기 없이 글자 변화로 기다리는가
  ③ 입찰해도 매물 가격은 그대로이고, 화면을 다시 열면 상태 칸이 비어도 기록은 남아 있는가

읽은 값은 읽는 즉시 판단하지 않고 변수에 모아 두고, 브라우저를 닫은 뒤 마지막에 한꺼번에 비교합니다.
중간에 assert 로 멈추면 두 번째 입찰까지 확인하지 못하고 스크린샷도 남지 않기 때문입니다.
"""
import time

from selenium.webdriver.common.by import By

from game_login import setup, save_screenshot, GAME_URL

# ── 기획 데이터 (화면에서 읽지 않고 기획서 값을 코드에 적습니다)
# 기획서 매물 표에서 이름에 「달빛」 이 든 매물 6건을 미리 계산해 두었습니다.
KEYWORD = "달빛"
SPEC_MOONLIGHT = ["A-02", "A-07", "A-11", "A-14", "A-17", "A-23"]
FIRST_LOT = "A-07"                                      # 달빛검
FIRST_PRICE = 4800                                      # 입찰 금액은 매물 가격 그대로입니다
SECOND_LOT = "A-11"                                     # 달빛 방패
CONFIRM_SECONDS = 3                                     # 접수에서 확정까지 걸리는 시간


def card_lot_numbers(driver):
    """지금 화면에 있는 결과 카드의 매물 번호 목록을 만듭니다 (TC-2-02)."""
    lot_numbers = []
    el_cards = driver.find_elements(By.CSS_SELECTOR, "#auc-list .auc-card")

    for el_card in el_cards:
        # 카드 id 는 auc-card-A-07 모양이라 앞부분을 떼어 매물 번호만 남깁니다
        card_id = el_card.get_attribute("id")
        lot_numbers.append(card_id.removeprefix("auc-card-"))
    return lot_numbers


def bid_state(driver, lot_no):
    """매물 1건의 상태 칸 글자를 반환합니다.

    카드가 없으면 빈 글자를 반환합니다.

    상태 칸은 카드를 만들 때 빈 칸으로 함께 생깁니다.
    다만 이 함수는 Wait 조건 안에서도 사용하므로, 카드가 아직 없는 순간에 호출될 수 있습니다.
    find_element 는 그때 NoSuchElementException 을 내므로 find_elements 로 찾습니다.
    """
    el_states = driver.find_elements(By.ID, f"bid-state-{lot_no}")

    if len(el_states) == 0:
        return ""
    return el_states[0].text


def all_bid_states(driver):
    """검색 결과 카드 전부의 상태를 {매물 번호: 상태} 딕셔너리로 모읍니다 (TC-2-07 · TC-2-08)."""
    states = {}
    for lot_no in card_lot_numbers(driver):
        states[lot_no] = bid_state(driver, lot_no)
    return states


def card_price(driver, lot_no):
    """카드 문구에서 가격만 정수로 뽑습니다.

    카드에는 등록일과 남은 기간처럼 다른 숫자도 함께 있습니다.
    쉼표를 지우고 칸 단위로 나눈 뒤 숫자로만 된 조각의 첫 번째가 가격입니다.
    """
    el_card = driver.find_element(By.ID, f"auc-card-{lot_no}")
    parts = el_card.text.replace(",", "").split()
    # 컴프리헨션으로 숫자 조각만 남긴 목록을 먼저 만듭니다.
    # 중간 목록이 변수로 남아, 값이 예상과 다를 때 numbers 를 출력해 확인할 수 있습니다
    numbers = [part for part in parts if part.isdigit()]

    if len(numbers) == 0:
        return None
    return int(numbers[0])


def search(driver, wait, keyword):
    """경매장을 열고 이름으로 검색한 뒤 결과가 올 때까지 기다립니다 (TC-2-01)."""
    driver.get(GAME_URL + "/auction")
    # wait.until 은 조건을 0.5초 간격으로 다시 실행해 참이 될 때까지 기다립니다.
    # 그래서 인자로 「값」 이 아니라 「호출할 함수」 를 전달해야 합니다.
    #   d.find_element(...).text != ""      ← 지금 시점에서 한 번 계산한 True/False 입니다
    #   lambda d: d.find_element(...).text != ""  ← 회차마다 다시 계산하는 함수입니다
    # lambda 는 이름 없는 함수라 def 로 따로 정의하지 않고 조건 1개를 그대로 작성할 수 있고,
    # 매개변수 d 에는 wait 를 만들 때 지정한 driver 가 회차마다 전달됩니다
    wait.until(lambda d: len(d.find_elements(By.ID, "auc-search")) > 0,
               message="경매장 검색 화면이 열리지 않음")

    el_name = driver.find_element(By.ID, "auc-name")
    el_name.clear()                                     # 화면을 다시 열어도 앞 검색어가 남을 수 있습니다
    el_name.send_keys(keyword)

    el_search_btn = driver.find_element(By.ID, "auc-search")
    el_search_btn.click()

    # 결과는 1.5초 뒤에 옵니다.
    # 기다리지 않으면 「검색 중...」 을 건수로 읽습니다.
    # 건수 문구는 회차마다 다시 읽어야 하므로 lambda 로 만든 조건 함수를 전달합니다
    wait.until(lambda d: "검색 결과" in d.find_element(By.ID, "auc-count").text,
               message="1.5초 뒤 검색 결과 건수 문구가 나오지 않음")


# =====================================================================
# 진행
# =====================================================================
driver, wait = setup()

# ── TC-2-01. 이름으로 검색한 뒤 건수 문구
search(driver, wait, KEYWORD)
el_count = driver.find_element(By.ID, "auc-count")
count_text = el_count.text

# ── TC-2-02. 결과 카드의 매물 번호
found_lots = card_lot_numbers(driver)

# ── TC-2-03. 입찰 전 상태 칸과 가격
state_before = bid_state(driver, FIRST_LOT)
price_before = card_price(driver, FIRST_LOT)

# ── TC-2-04. 입찰 직후 상태와 결과 문구
# 확정까지 걸린 시간을 재려면 누르기 직전 시각이 필요합니다
started = time.time()
el_bid_btn = driver.find_element(By.ID, f"bid-btn-{FIRST_LOT}")
el_bid_btn.click()

# 상태 칸이 채워질 때까지 기다립니다.
# 기다리지 않으면 빈 칸을 읽어 접수 상태를 확인하지 못합니다
# 조건 안에서 bid_state() 를 부르면 회차마다 상태 칸을 다시 읽습니다
wait.until(lambda d: bid_state(d, FIRST_LOT) != "",
           message="입찰 상태 칸이 채워지지 않음")

state_received = bid_state(driver, FIRST_LOT)
el_msg = driver.find_element(By.ID, "auc-msg")
bid_msg = el_msg.text

# ── TC-2-05. 3초 뒤 확정으로 바뀌는지
# time.sleep(3) 으로 세면 서버가 느린 경우 아직 접수인 상태를 읽어 실패로 판정합니다.
# 글자가 확정이 되는 것을 조건으로 두면 빠르든 느리든 같은 결과가 나옵니다
# 「확정이 될 때까지」 를 함수로 전달해, 3초가 지나 글자가 바뀌는 회차에 기다림이 끝납니다
wait.until(lambda d: bid_state(d, FIRST_LOT) == "확정",
           message="입찰이 3초 뒤에도 확정으로 바뀌지 않음")

seconds_to_confirm = time.time() - started
state_confirmed = bid_state(driver, FIRST_LOT)

# ── TC-2-06. 확정 뒤 매물 가격
price_after = card_price(driver, FIRST_LOT)

el_first_card = driver.find_element(By.ID, f"auc-card-{FIRST_LOT}")
shot_first = save_screenshot(driver, "02_첫_입찰_확정", el_first_card)

# ── TC-2-07. 화면을 다시 열었을 때의 상태 칸
# 경매장 화면은 그 화면에서 입찰한 매물만 상태 칸에 표시합니다.
# 비어 있는 것 자체가 기대값이며, 기록이 사라진 것이 아닙니다
search(driver, wait, KEYWORD)
states_after_reload = all_bid_states(driver)
price_after_reload = card_price(driver, FIRST_LOT)

# ── TC-2-08. 다른 매물에 입찰하면 앞 입찰 상태까지 다시 표시되는지
# 화면이 내 입찰 기록 전체를 다시 읽기 때문에, 비어 있던 A-07 도 확정으로 표시됩니다.
# 이것이 기록이 서버에 남아 있다는 화면상의 증거입니다
el_second_btn = driver.find_element(By.ID, f"bid-btn-{SECOND_LOT}")
el_second_btn.click()
# 두 번째 입찰도 같은 조건 함수를 매물 번호만 바꿔 전달합니다
wait.until(lambda d: bid_state(d, SECOND_LOT) == "확정",
           message="두 번째 입찰이 확정으로 바뀌지 않음")

states_after_second = all_bid_states(driver)

el_list = driver.find_element(By.ID, "auc-list")
shot_second = save_screenshot(driver, "02_두_입찰_상태", el_list)

driver.quit()

print(f"{count_text} · 카드 {found_lots}")
print(f"입찰 전 · 상태 {state_before!r} · 가격 {price_before}")
print(f"입찰 직후 · 상태 {state_received!r} · 문구 {bid_msg!r}")
print(f"확정 · 상태 {state_confirmed!r} · 가격 {price_after}")
print(f"다시 연 뒤 · 상태 {states_after_reload} · 가격 {price_after_reload}")
print(f"두 번째 입찰 뒤 · 상태 {states_after_second}")


# =====================================================================
# 검증 (브라우저를 닫은 뒤 모아 둔 값을 한꺼번에 비교합니다)
# =====================================================================
# TC-2-01 · TC-2-02. 건수 문구와 매물 번호를 기획서 표로 센 값과 비교합니다
assert count_text == f"검색 결과 {len(SPEC_MOONLIGHT)}건", \
    f"건수 문구: 기대 '검색 결과 {len(SPEC_MOONLIGHT)}건', 실제 {count_text!r}"
assert found_lots == SPEC_MOONLIGHT, f"검색 결과 매물: 기대 {SPEC_MOONLIGHT}, 실제 {found_lots}"

# TC-2-03. 입찰 전 상태 칸은 빈 글자입니다
assert state_before == "", f"입찰 전 상태 칸: 기대 '', 실제 {state_before!r}"

# TC-2-04. 누르자마자 확정이 아니라 접수입니다
assert state_received == "접수", f"입찰 직후 상태: 기대 '접수', 실제 {state_received!r}"
assert bid_msg == f"입찰 접수: {FIRST_LOT} {FIRST_PRICE}G", f"입찰 결과 문구: 실제 {bid_msg!r}"

# TC-2-05. 확정까지 3초 이상 걸립니다.
# 걸린 시간을 확인하지 않으면 확정 상태만 보고 우연히 통과할 수 있습니다
assert state_confirmed == "확정", f"3초 뒤 상태: 기대 '확정', 실제 {state_confirmed!r}"
assert seconds_to_confirm >= CONFIRM_SECONDS, \
    f"확정까지 걸린 시간: 기대 {CONFIRM_SECONDS}초 이상, 실제 {seconds_to_confirm:.1f}초"

# TC-2-06. 입찰해도 매물 가격은 그대로입니다
assert price_before == price_after == price_after_reload == FIRST_PRICE, \
    f"매물 가격: 기대 {FIRST_PRICE} 유지, 실제 {price_before} → {price_after} → {price_after_reload}"

# TC-2-07. 다시 연 화면에서는 상태 칸 6개가 모두 비어 있습니다.
# 비어 있지 않은 매물만 모아 두면 어느 것이 다른지 메시지에 남습니다
# 「전부 비어 있는가」 를 참·거짓 1개로 확인하면 어느 매물이 다른지 메시지에 남지 않습니다.
# 컴프리헨션으로 비어 있지 않은 매물만 모아 두면 개수로 판정하면서 목록도 그대로 보고할 수 있습니다
filled_after_reload = [lot for lot in states_after_reload if states_after_reload[lot] != ""]
assert len(filled_after_reload) == 0, \
    f"다시 연 뒤 상태 칸: 기대 모두 '', 실제 {states_after_reload}"
assert len(states_after_reload) == len(SPEC_MOONLIGHT), \
    f"다시 연 뒤 카드 수: 기대 {len(SPEC_MOONLIGHT)}, 실제 {len(states_after_reload)}"

# TC-2-08. 두 번째 입찰 뒤에는 입찰한 매물 2건만 확정입니다
expected_second = {}
for lot in SPEC_MOONLIGHT:
    expected_second[lot] = ""
expected_second[FIRST_LOT] = "확정"
expected_second[SECOND_LOT] = "확정"

assert states_after_second == expected_second, \
    f"두 번째 입찰 뒤 상태: 기대 {expected_second}, 실제 {states_after_second}"

# 스크린샷 2개가 실제로 저장되었는지 확인합니다 (save_screenshot 이 파일 경로를 반환합니다)
import os
# 없는 파일만 모아 개수로 판정하면 어느 스크린샷이 없는지 메시지에 남습니다
missing_shots = [path for path in [shot_first, shot_second] if not os.path.exists(path)]
assert len(missing_shots) == 0, f"스크린샷이 없습니다: {missing_shots}"

print("게임 실습 2 정답 통과")
