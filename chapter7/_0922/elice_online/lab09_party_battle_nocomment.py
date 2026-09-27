import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from game_login import setup, make_wait, close_dialog, save_screenshot, GAME_URL

SPEC_HEROES = [{"hero_id": "h1", "name": "루앤", "job": "검사", "power": 40},
               {"hero_id": "h2", "name": "미르", "job": "궁수", "power": 35},
               {"hero_id": "h3", "name": "노아", "job": "사제", "power": 25},
               {"hero_id": "h4", "name": "세라", "job": "마법사", "power": 45},
               {"hero_id": "h5", "name": "카이", "job": "도적", "power": 30}]
NEED_POWER = 100
MATCH_SECONDS = 5
WIN_SCORE = 1000

DAGGER_ID = 11
DAGGER_NAME = "견습 단검"
MAIN_TITLE = "모험가의 거점"
LOCK_MSG = "무기를 장착하면 전투 준비가 열립니다"
MSG_NOT_FULL = "파티 3명을 모두 골라야 합니다"
MSG_DUPLICATED = "같은 영웅을 두 번 고를 수 없습니다"
STATE_MATCHED = "매칭 완료"

HERO_POWER = {}
HERO_NAME = {}
for hero in SPEC_HEROES:
    HERO_POWER[hero["hero_id"]] = hero["power"]
    HERO_NAME[hero["hero_id"]] = hero["name"]

ONE_PICK = ["h1", "", ""]
DUPLICATED_PICK = ["h1", "h1", "h2"]
LOSE_PICK = ["h3", "h5", "h2"]
WIN_PICK = ["h1", "h4", "h2"]


def step(title):
    print(f"\n=== {title} ===")


def power_sum(picked):
    return sum([HERO_POWER.get(hero_id, 0) for hero_id in picked])


def names_of(picked):
    return [HERO_NAME[hero_id] for hero_id in picked if hero_id != ""]


def rgb_of(el):
    text = el.value_of_css_property("color")
    inside = text.split("(")[1].split(")")[0]
    numbers = [int(float(part)) for part in inside.split(",")]
    return tuple(numbers[:3])


def read_battle_menu(driver):
    el_menu = driver.find_element(By.ID, "menu-battle")
    el_lock_msg = driver.find_element(By.ID, "battle-lock-msg")
    return {"class": el_menu.get_attribute("class"),
            "aria": el_menu.get_attribute("aria-disabled"),
            "color": rgb_of(el_menu),
            "lock_msg_shown": el_lock_msg.is_displayed(),
            "lock_msg": el_lock_msg.text}


def pick_party(driver, wait, picked):
    for number in [1, 2, 3]:
        el_slot = driver.find_element(By.ID, f"party-slot-{number}")
        Select(el_slot).select_by_value(picked[number - 1])

    expected = str(power_sum(picked))
    wait.until(EC.text_to_be_present_in_element((By.ID, "party-power"), expected),
               message=f"전투력 합이 {expected} 로 다시 계산되지 않음")


def read_party_state(driver):
    el_power = driver.find_element(By.ID, "party-power")
    el_start_btn = driver.find_element(By.ID, "battle-start")
    el_msg = driver.find_element(By.ID, "battle-msg")
    return {"sum": el_power.text,
            "btn_enabled": el_start_btn.is_enabled(),
            "msg": el_msg.text}


def fight(driver, wait):
    el_start_btn = driver.find_element(By.ID, "battle-start")
    started_at = time.time()
    el_start_btn.click()

    wait.until(lambda d: d.find_element(By.ID, "battle-result").text != "",
               message="전투 결과가 나오지 않음")
    elapsed = round(time.time() - started_at, 1)

    el_result = driver.find_element(By.ID, "battle-result")
    el_state = driver.find_element(By.ID, "battle-state")
    el_elapsed = driver.find_element(By.ID, "battle-elapsed")
    result_text = el_result.text
    state_text = el_state.text
    waited_text = el_elapsed.text

    dialog_title, _ = close_dialog(driver, wait)

    return {"dialog": dialog_title,
            "result": result_text,
            "state": state_text,
            "waited": waited_text,
            "elapsed": elapsed}


driver, _ = setup()
wait = make_wait(driver, 20)

step("무기 장착 전 · 전투 준비 메뉴 상태")
driver.get(GAME_URL + "/main")
wait.until(EC.text_to_be_present_in_element((By.ID, "main-title"), MAIN_TITLE),
           message="메인 화면이 열리지 않음")

menu_before = read_battle_menu(driver)
shot_locked = save_screenshot(driver, "09_장착_전_메뉴_잠김")
print(menu_before)

el_menu_battle = driver.find_element(By.ID, "menu-battle")
el_menu_battle.click()
el_main_title = driver.find_element(By.ID, "main-title")
url_after_click = driver.current_url
title_after_click = el_main_title.text
print(f"비활성 메뉴를 누른 뒤 주소 {url_after_click} · 제목 {title_after_click!r}")

step(f"{DAGGER_NAME} 구매와 장착")
driver.get(GAME_URL + "/shop")
el_buy_btn = wait.until(EC.element_to_be_clickable((By.ID, f"buy-btn-{DAGGER_ID}")),
                        message="구매 버튼이 준비되지 않음")
el_buy_btn.click()
wait.until(lambda d: d.find_element(By.ID, "shop-msg").text != "",
           message="구매 결과 문구가 나오지 않음")
el_shop_msg = driver.find_element(By.ID, "shop-msg")
buy_msg = el_shop_msg.text
close_dialog(driver, wait)
print(f"구매: {buy_msg}")

driver.get(GAME_URL + "/inventory")
el_row = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, f"//table[@id='inv-table']/tbody/tr[td[@class='col-name'][normalize-space()='{DAGGER_NAME}']]")),
    message="보유 아이템 표에 구매한 무기가 없음")
row_id = el_row.get_attribute("data-row-id")
el_equip_btn = driver.find_element(By.ID, f"eq-btn-{row_id}")
el_equip_btn.click()
wait.until(EC.text_to_be_present_in_element((By.ID, "equip-weapon"), DAGGER_NAME),
           message="장착 무기 글자가 바뀌지 않음")
el_equip_weapon = driver.find_element(By.ID, "equip-weapon")
equipped_weapon = el_equip_weapon.text
print(f"장착 무기: {equipped_weapon}")

step("무기 장착 뒤 · 전투 준비 메뉴 상태")
driver.get(GAME_URL + "/main")
wait.until(EC.text_to_be_present_in_element((By.ID, "main-title"), MAIN_TITLE),
           message="메인 화면이 열리지 않음")
menu_after = read_battle_menu(driver)
print(menu_after)

el_menu_battle = driver.find_element(By.ID, "menu-battle")
el_menu_battle.click()
wait.until(EC.presence_of_element_located((By.ID, "battle-start")),
           message="전투 준비 화면이 열리지 않음")
prepare_url = driver.current_url
print(f"전투 준비 화면 주소: {prepare_url}")

step("출전 버튼 활성 조건 확인")
pick_party(driver, wait, ONE_PICK)
one_pick_state = read_party_state(driver)
print(f"한 칸만 고름: {one_pick_state}")

pick_party(driver, wait, DUPLICATED_PICK)
duplicated_state = read_party_state(driver)
print(f"같은 영웅 두 번: {duplicated_state}")

step("패배 파티로 출전")
pick_party(driver, wait, LOSE_PICK)
lose_party_state = read_party_state(driver)
print(f"파티: {names_of(LOSE_PICK)} {lose_party_state}")
lose_result = fight(driver, wait)
print(lose_result)

step("승리 파티로 출전")
pick_party(driver, wait, WIN_PICK)
win_party_state = read_party_state(driver)
print(f"파티: {names_of(WIN_PICK)} {win_party_state}")
win_result = fight(driver, wait)
shot_win = save_screenshot(driver, "09_승리_결과")
print(win_result)

step("승리 뒤 내 점수 확인")
driver.get(GAME_URL + "/ranking")
wait.until(lambda d: d.find_element(By.ID, "my-rank").text != "",
           message="내 순위 문구가 나오지 않음")
el_my_rank = driver.find_element(By.ID, "my-rank")
my_rank_text = el_my_rank.text
print(my_rank_text)

driver.quit()


assert "disabled" in menu_before["class"] and menu_before["aria"] == "true", \
    (f"장착 전 전투 준비 메뉴: 기대 class 에 'disabled' 포함·aria 'true', "
     f"실제 {menu_before['class']!r}·{menu_before['aria']!r}")
assert menu_before["lock_msg_shown"], "장착 전 잠금 안내가 보이지 않습니다"
assert menu_before["lock_msg"] == LOCK_MSG, \
    f"잠금 안내 문구: 기대 {LOCK_MSG!r}, 실제 {menu_before['lock_msg']!r}"

assert menu_before["color"] == menu_after["color"], \
    f"잠김과 열림의 글자 색: 기대 같은 값, 실제 {menu_before['color']}·{menu_after['color']}"

assert url_after_click.endswith("/main") and title_after_click == MAIN_TITLE, \
    f"비활성 메뉴를 누른 뒤: 기대 /main 그대로, 실제 {url_after_click} {title_after_click!r}"

assert buy_msg == f"구매 완료: {DAGGER_NAME} x1", f"구매 결과 문구: 실제 {buy_msg!r}"
assert equipped_weapon == DAGGER_NAME, f"장착 무기: 기대 {DAGGER_NAME!r}, 실제 {equipped_weapon!r}"
assert "disabled" not in menu_after["class"] and menu_after["aria"] == "false", \
    (f"장착 뒤 전투 준비 메뉴: 기대 class 에 'disabled' 없음·aria 'false', "
     f"실제 {menu_after['class']!r}·{menu_after['aria']!r}")
assert menu_after["lock_msg_shown"] is False, "장착 뒤에도 잠금 안내가 보입니다"
assert prepare_url.endswith("/battle/prepare"), \
    f"전투 준비 화면 주소: 기대 /battle/prepare, 실제 {prepare_url}"

assert one_pick_state == {"sum": str(power_sum(ONE_PICK)),
                          "btn_enabled": False,
                          "msg": MSG_NOT_FULL}, f"한 칸만 고른 상태: 실제 {one_pick_state}"

assert duplicated_state == {"sum": str(power_sum(DUPLICATED_PICK)),
                            "btn_enabled": False,
                            "msg": MSG_DUPLICATED}, f"같은 영웅 두 번 고른 상태: 실제 {duplicated_state}"

lose_sum = power_sum(LOSE_PICK)
win_sum = power_sum(WIN_PICK)
assert lose_party_state == {"sum": str(lose_sum), "btn_enabled": True, "msg": ""}, \
    f"패배 파티 상태: 실제 {lose_party_state}"
assert win_party_state == {"sum": str(win_sum), "btn_enabled": True, "msg": ""}, \
    f"승리 파티 상태: 실제 {win_party_state}"

assert lose_result["result"] == f"패배 · 전투력 {lose_sum} / 요구 {NEED_POWER}", \
    (f"패배 결과 문구: 기대 '패배 · 전투력 {lose_sum} / 요구 {NEED_POWER}', "
     f"실제 {lose_result['result']!r}")
assert win_result["result"] == f"승리 · 전투력 {win_sum} / 요구 {NEED_POWER}", \
    (f"승리 결과 문구: 기대 '승리 · 전투력 {win_sum} / 요구 {NEED_POWER}', "
     f"실제 {win_result['result']!r}")
assert lose_result["dialog"] == "전투 패배", f"패배 Dialog 제목: 실제 {lose_result['dialog']!r}"
assert win_result["dialog"] == "전투 승리!", f"승리 Dialog 제목: 실제 {win_result['dialog']!r}"
assert lose_result["state"] == win_result["state"] == STATE_MATCHED, \
    (f"전투 상태: 기대 {STATE_MATCHED!r}, "
     f"실제 패배 {lose_result['state']!r}·승리 {win_result['state']!r}")

assert lose_result["elapsed"] >= MATCH_SECONDS and win_result["elapsed"] >= MATCH_SECONDS, \
    (f"매칭 대기: 기대 {MATCH_SECONDS}초 이상, "
     f"실제 패배 {lose_result['elapsed']}초·승리 {win_result['elapsed']}초")

assert my_rank_text == f"내 점수 {WIN_SCORE} · 순위 밖", f"내 순위 문구: 실제 {my_rank_text!r}"

import os
missing_shots = [path for path in [shot_locked, shot_win] if not os.path.exists(path)]
assert len(missing_shots) == 0, f"스크린샷이 없습니다: {missing_shots}"

print("게임 실습 9 정답 통과")
