import time

from selenium.webdriver.common.by import By

from game_login import setup, save_screenshot, GAME_URL

KEYWORD = "달빛"
SPEC_MOONLIGHT = ["A-02", "A-07", "A-11", "A-14", "A-17", "A-23"]
FIRST_LOT = "A-07"
FIRST_PRICE = 4800
SECOND_LOT = "A-11"
CONFIRM_SECONDS = 3


def card_lot_numbers(driver):
    lot_numbers = []
    el_cards = driver.find_elements(By.CSS_SELECTOR, "#auc-list .auc-card")

    for el_card in el_cards:
        card_id = el_card.get_attribute("id")
        lot_numbers.append(card_id.removeprefix("auc-card-"))
    return lot_numbers


def bid_state(driver, lot_no):
    el_states = driver.find_elements(By.ID, f"bid-state-{lot_no}")

    if len(el_states) == 0:
        return ""
    return el_states[0].text


def all_bid_states(driver):
    states = {}
    for lot_no in card_lot_numbers(driver):
        states[lot_no] = bid_state(driver, lot_no)
    return states


def card_price(driver, lot_no):
    el_card = driver.find_element(By.ID, f"auc-card-{lot_no}")
    parts = el_card.text.replace(",", "").split()
    numbers = [part for part in parts if part.isdigit()]

    if len(numbers) == 0:
        return None
    return int(numbers[0])


def search(driver, wait, keyword):
    driver.get(GAME_URL + "/auction")
    wait.until(lambda d: len(d.find_elements(By.ID, "auc-search")) > 0,
               message="경매장 검색 화면이 열리지 않음")

    el_name = driver.find_element(By.ID, "auc-name")
    el_name.clear()
    el_name.send_keys(keyword)

    el_search_btn = driver.find_element(By.ID, "auc-search")
    el_search_btn.click()

    wait.until(lambda d: "검색 결과" in d.find_element(By.ID, "auc-count").text,
               message="1.5초 뒤 검색 결과 건수 문구가 나오지 않음")


driver, wait = setup()

search(driver, wait, KEYWORD)
el_count = driver.find_element(By.ID, "auc-count")
count_text = el_count.text

found_lots = card_lot_numbers(driver)

state_before = bid_state(driver, FIRST_LOT)
price_before = card_price(driver, FIRST_LOT)

started = time.time()
el_bid_btn = driver.find_element(By.ID, f"bid-btn-{FIRST_LOT}")
el_bid_btn.click()

wait.until(lambda d: bid_state(d, FIRST_LOT) != "",
           message="입찰 상태 칸이 채워지지 않음")

state_received = bid_state(driver, FIRST_LOT)
el_msg = driver.find_element(By.ID, "auc-msg")
bid_msg = el_msg.text

wait.until(lambda d: bid_state(d, FIRST_LOT) == "확정",
           message="입찰이 3초 뒤에도 확정으로 바뀌지 않음")

seconds_to_confirm = time.time() - started
state_confirmed = bid_state(driver, FIRST_LOT)

price_after = card_price(driver, FIRST_LOT)

el_first_card = driver.find_element(By.ID, f"auc-card-{FIRST_LOT}")
shot_first = save_screenshot(driver, "02_첫_입찰_확정", el_first_card)

search(driver, wait, KEYWORD)
states_after_reload = all_bid_states(driver)
price_after_reload = card_price(driver, FIRST_LOT)

el_second_btn = driver.find_element(By.ID, f"bid-btn-{SECOND_LOT}")
el_second_btn.click()
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


assert count_text == f"검색 결과 {len(SPEC_MOONLIGHT)}건", \
    f"건수 문구: 기대 '검색 결과 {len(SPEC_MOONLIGHT)}건', 실제 {count_text!r}"
assert found_lots == SPEC_MOONLIGHT, f"검색 결과 매물: 기대 {SPEC_MOONLIGHT}, 실제 {found_lots}"

assert state_before == "", f"입찰 전 상태 칸: 기대 '', 실제 {state_before!r}"

assert state_received == "접수", f"입찰 직후 상태: 기대 '접수', 실제 {state_received!r}"
assert bid_msg == f"입찰 접수: {FIRST_LOT} {FIRST_PRICE}G", f"입찰 결과 문구: 실제 {bid_msg!r}"

assert state_confirmed == "확정", f"3초 뒤 상태: 기대 '확정', 실제 {state_confirmed!r}"
assert seconds_to_confirm >= CONFIRM_SECONDS, \
    f"확정까지 걸린 시간: 기대 {CONFIRM_SECONDS}초 이상, 실제 {seconds_to_confirm:.1f}초"

assert price_before == price_after == price_after_reload == FIRST_PRICE, \
    f"매물 가격: 기대 {FIRST_PRICE} 유지, 실제 {price_before} → {price_after} → {price_after_reload}"

filled_after_reload = [lot for lot in states_after_reload if states_after_reload[lot] != ""]
assert len(filled_after_reload) == 0, \
    f"다시 연 뒤 상태 칸: 기대 모두 '', 실제 {states_after_reload}"
assert len(states_after_reload) == len(SPEC_MOONLIGHT), \
    f"다시 연 뒤 카드 수: 기대 {len(SPEC_MOONLIGHT)}, 실제 {len(states_after_reload)}"

expected_second = {}
for lot in SPEC_MOONLIGHT:
    expected_second[lot] = ""
expected_second[FIRST_LOT] = "확정"
expected_second[SECOND_LOT] = "확정"

assert states_after_second == expected_second, \
    f"두 번째 입찰 뒤 상태: 기대 {expected_second}, 실제 {states_after_second}"

import os
missing_shots = [path for path in [shot_first, shot_second] if not os.path.exists(path)]
assert len(missing_shots) == 0, f"스크린샷이 없습니다: {missing_shots}"

print("게임 실습 2 정답 통과")
