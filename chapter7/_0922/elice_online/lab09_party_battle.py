"""실습 9. 파티 편성과 출전 버튼 상태, 매칭 대기 · 정답 코드와 해설

화면 /main · /battle/prepare        테스트 케이스 8개 (TC-9-01 ~ TC-9-08)

이 실습이 확인하는 것은 3가지입니다.
  ① 잠김과 열림을 글자 색이 아니라 class 와 aria-disabled 로 판정하는가
  ② 출전 버튼의 활성 조건 3가지를 안내 문구와 함께 확인하는가
  ③ 매칭 5초를 세어 두지 않고 결과 문구를 기다린 뒤 걸린 시간을 재는가

승패 기대값은 화면에서 가져오지 않고 기획서 영웅 표의 전투력을 더해 먼저 만듭니다.
"""
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from game_login import setup, make_wait, close_dialog, save_screenshot, GAME_URL

# ── 기획 데이터 (화면에서 읽지 않고 기획서 값을 코드에 적습니다)
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

# 영웅 번호로 전투력과 이름을 바로 찾을 수 있게 딕셔너리 2개를 만들어 둡니다.
# 목록을 그때그때 뒤지면 같은 검색이 여러 곳에 흩어집니다
HERO_POWER = {}
HERO_NAME = {}
for hero in SPEC_HEROES:
    HERO_POWER[hero["hero_id"]] = hero["power"]
    HERO_NAME[hero["hero_id"]] = hero["name"]

ONE_PICK = ["h1", "", ""]                 # TC-9-04. 한 칸만 고른 파티입니다
DUPLICATED_PICK = ["h1", "h1", "h2"]      # TC-9-05. 같은 영웅을 두 번 고른 파티입니다
LOSE_PICK = ["h3", "h5", "h2"]            # TC-9-06. 25 + 30 + 35 = 90 으로 요구 전투력에 못 미칩니다
WIN_PICK = ["h1", "h4", "h2"]             # TC-9-07. 40 + 45 + 35 = 120 으로 요구 전투력을 넘습니다


def step(title):
    """진행 단계를 출력합니다.

    어느 단계의 값인지 출력에서 구분하기 위해서입니다.
    """
    print(f"\n=== {title} ===")


def power_sum(picked):
    """기획서 전투력으로 파티 합을 계산합니다.

    빈 칸은 0으로 셉니다.
    화면의 합을 기대값으로 쓰면 화면이 틀렸을 때 확인이 되지 않습니다.
    """
    return sum([HERO_POWER.get(hero_id, 0) for hero_id in picked])


def names_of(picked):
    """영웅 번호 목록을 이름 목록으로 바꿉니다.

    출력에 h1 대신 이름이 남아 어떤 파티였는지 알 수 있습니다.
    """
    return [HERO_NAME[hero_id] for hero_id in picked if hero_id != ""]


def rgb_of(el):
    """요소의 글자 색을 (R, G, B) 3가지 값으로 바꿉니다.

    value_of_css_property 는 'rgba(170, 180, 184, 1)' 같은 글자를 반환합니다.
    숫자만 꺼내 비교할 수 있는 모양으로 만듭니다.
    """
    text = el.value_of_css_property("color")
    inside = text.split("(")[1].split(")")[0]
    numbers = [int(float(part)) for part in inside.split(",")]
    return tuple(numbers[:3])


def read_battle_menu(driver):
    """전투 준비 메뉴의 상태를 딕셔너리 하나로 모읍니다 (TC-9-01 · TC-9-03).

    색도 함께 읽어 두지만 판정에는 쓰지 않습니다.
    잠김과 열림의 색이 같다는 것을 출력으로 남기기 위해서입니다.
    """
    el_menu = driver.find_element(By.ID, "menu-battle")
    el_lock_msg = driver.find_element(By.ID, "battle-lock-msg")
    return {"class": el_menu.get_attribute("class"),
            "aria": el_menu.get_attribute("aria-disabled"),
            "color": rgb_of(el_menu),
            "lock_msg_shown": el_lock_msg.is_displayed(),
            "lock_msg": el_lock_msg.text}


def pick_party(driver, wait, picked):
    """파티 3칸을 고르고 전투력 합이 다시 계산될 때까지 기다립니다 (TC-9-04 ~ TC-9-07)."""
    for number in [1, 2, 3]:
        el_slot = driver.find_element(By.ID, f"party-slot-{number}")
        # select 는 click 과 send_keys 로 다루면 브라우저마다 다르게 움직입니다.
        # Select 로 값을 지정하면 change 가 함께 일어나 화면이 다시 계산됩니다
        Select(el_slot).select_by_value(picked[number - 1])

    # 칸을 고친 직후에 버튼 상태를 읽으면 다시 계산되기 전 값을 읽습니다.
    # 합이 기획서로 계산한 값이 되는 것을 신호로 삼습니다
    expected = str(power_sum(picked))
    wait.until(EC.text_to_be_present_in_element((By.ID, "party-power"), expected),
               message=f"전투력 합이 {expected} 로 다시 계산되지 않음")


def read_party_state(driver):
    """전투력 합 · 출전 버튼 활성 여부 · 안내 문구를 딕셔너리로 모읍니다."""
    el_power = driver.find_element(By.ID, "party-power")
    el_start_btn = driver.find_element(By.ID, "battle-start")
    el_msg = driver.find_element(By.ID, "battle-msg")
    return {"sum": el_power.text,
            "btn_enabled": el_start_btn.is_enabled(),
            "msg": el_msg.text}


def fight(driver, wait):
    """출전해서 결과 문구를 기다린 뒤 결과 · 상태 · 대기 초 · 걸린 시간을 모읍니다.

    5초를 세어 두면 화면이 늦을 때 값을 잘못 읽습니다.
    결과 문구가 채워지는 것을 기다리고 걸린 시간을 재어 확인합니다.
    """
    el_start_btn = driver.find_element(By.ID, "battle-start")
    started_at = time.time()          # 기다림이 끝난 뒤 뺄셈에 쓰려고 누른 시각을 보관합니다
    el_start_btn.click()

    # 전투 상태 글자에는 앞 전투의 「매칭 완료」 가 잠시 남습니다.
    # 그래서 상태가 아니라 결과 문구가 채워지는 것을 조건으로 씁니다
    wait.until(lambda d: d.find_element(By.ID, "battle-result").text != "",
               message="전투 결과가 나오지 않음")
    elapsed = round(time.time() - started_at, 1)

    el_result = driver.find_element(By.ID, "battle-result")
    el_state = driver.find_element(By.ID, "battle-state")
    el_elapsed = driver.find_element(By.ID, "battle-elapsed")
    result_text = el_result.text
    state_text = el_state.text
    waited_text = el_elapsed.text

    # Dialog 를 닫지 않고 다음 출전을 누르면 ElementClickInterceptedException 이 발생합니다.
    # 제공 코드의 close_dialog 가 제목과 본문을 반환하면서 창을 닫아 줍니다
    dialog_title, _ = close_dialog(driver, wait)

    return {"dialog": dialog_title,
            "result": result_text,
            "state": state_text,
            "waited": waited_text,
            "elapsed": elapsed}


# =====================================================================
# 진행
# =====================================================================
driver, _ = setup()
# 매칭에 5초가 걸리므로 기다리는 시간을 20초로 정한 Wait 를 사용합니다
wait = make_wait(driver, 20)

# ── TC-9-01. 무기를 장착하기 전 메뉴 상태
step("무기 장착 전 · 전투 준비 메뉴 상태")
driver.get(GAME_URL + "/main")
# 제목이 바뀌기 전에 읽으면 앞 화면의 값을 메인 화면 값으로 확인합니다
wait.until(EC.text_to_be_present_in_element((By.ID, "main-title"), MAIN_TITLE),
           message="메인 화면이 열리지 않음")

menu_before = read_battle_menu(driver)
shot_locked = save_screenshot(driver, "09_장착_전_메뉴_잠김")
print(menu_before)

# ── TC-9-02. 잠긴 메뉴를 눌러도 화면이 그대로인지
el_menu_battle = driver.find_element(By.ID, "menu-battle")
el_menu_battle.click()
el_main_title = driver.find_element(By.ID, "main-title")
url_after_click = driver.current_url
title_after_click = el_main_title.text
print(f"비활성 메뉴를 누른 뒤 주소 {url_after_click} · 제목 {title_after_click!r}")

# ── TC-9-03. 무기를 사고 장착한 뒤 메뉴 상태
step(f"{DAGGER_NAME} 구매와 장착")
driver.get(GAME_URL + "/shop")
el_buy_btn = wait.until(EC.element_to_be_clickable((By.ID, f"buy-btn-{DAGGER_ID}")),
                        message="구매 버튼이 준비되지 않음")
el_buy_btn.click()
# 결과 문구를 기다리지 않고 다음 화면으로 가면 Dialog 가 남아 다음 버튼이 눌리지 않습니다
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
# 가방 칸에는 id 가 없고 data-row-id 만 있습니다.
# 표에서 번호를 얻어 그 행의 장착 버튼 id 를 만듭니다
row_id = el_row.get_attribute("data-row-id")
el_equip_btn = driver.find_element(By.ID, f"eq-btn-{row_id}")
el_equip_btn.click()
# 장착 요약이 바뀌기 전에 메인 화면을 다시 열면 장착 전 상태의 메뉴를 읽습니다
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

# ── TC-9-04 · TC-9-05. 출전 버튼 활성 조건
step("출전 버튼 활성 조건 확인")
pick_party(driver, wait, ONE_PICK)
one_pick_state = read_party_state(driver)
print(f"한 칸만 고름: {one_pick_state}")

pick_party(driver, wait, DUPLICATED_PICK)
duplicated_state = read_party_state(driver)
print(f"같은 영웅 두 번: {duplicated_state}")

# ── TC-9-06. 패배 파티
step("패배 파티로 출전")
pick_party(driver, wait, LOSE_PICK)
lose_party_state = read_party_state(driver)
print(f"파티: {names_of(LOSE_PICK)} {lose_party_state}")
lose_result = fight(driver, wait)
print(lose_result)

# ── TC-9-07. 승리 파티
step("승리 파티로 출전")
pick_party(driver, wait, WIN_PICK)
win_party_state = read_party_state(driver)
print(f"파티: {names_of(WIN_PICK)} {win_party_state}")
win_result = fight(driver, wait)
shot_win = save_screenshot(driver, "09_승리_결과")
print(win_result)

# ── TC-9-08. 승리 뒤 내 점수
step("승리 뒤 내 점수 확인")
driver.get(GAME_URL + "/ranking")
# 내 순위 문구는 목록 응답이 온 뒤에 채워집니다.
# 기다리지 않고 읽으면 빈 글자를 점수로 확인합니다
wait.until(lambda d: d.find_element(By.ID, "my-rank").text != "",
           message="내 순위 문구가 나오지 않음")
el_my_rank = driver.find_element(By.ID, "my-rank")
my_rank_text = el_my_rank.text
print(my_rank_text)

driver.quit()


# =====================================================================
# 검증 (브라우저를 닫은 뒤 모아 둔 값을 한꺼번에 비교합니다)
# =====================================================================
# TC-9-01. 잠긴 메뉴는 class 와 aria-disabled 로 판정합니다
assert "disabled" in menu_before["class"] and menu_before["aria"] == "true", \
    (f"장착 전 전투 준비 메뉴: 기대 class 에 'disabled' 포함·aria 'true', "
     f"실제 {menu_before['class']!r}·{menu_before['aria']!r}")
assert menu_before["lock_msg_shown"], "장착 전 잠금 안내가 보이지 않습니다"
assert menu_before["lock_msg"] == LOCK_MSG, \
    f"잠금 안내 문구: 기대 {LOCK_MSG!r}, 실제 {menu_before['lock_msg']!r}"

# 색은 두 상태가 같습니다.
# 이 값이 같다는 것을 확인해 두면 「색으로 판정하면 안 된다」 는 근거가 남습니다
assert menu_before["color"] == menu_after["color"], \
    f"잠김과 열림의 글자 색: 기대 같은 값, 실제 {menu_before['color']}·{menu_after['color']}"

# TC-9-02. 비활성 메뉴를 눌러도 주소와 제목이 그대로입니다
assert url_after_click.endswith("/main") and title_after_click == MAIN_TITLE, \
    f"비활성 메뉴를 누른 뒤: 기대 /main 그대로, 실제 {url_after_click} {title_after_click!r}"

# TC-9-03. 장착한 뒤에는 class 에서 disabled 가 없어지고 안내가 숨습니다
assert buy_msg == f"구매 완료: {DAGGER_NAME} x1", f"구매 결과 문구: 실제 {buy_msg!r}"
assert equipped_weapon == DAGGER_NAME, f"장착 무기: 기대 {DAGGER_NAME!r}, 실제 {equipped_weapon!r}"
assert "disabled" not in menu_after["class"] and menu_after["aria"] == "false", \
    (f"장착 뒤 전투 준비 메뉴: 기대 class 에 'disabled' 없음·aria 'false', "
     f"실제 {menu_after['class']!r}·{menu_after['aria']!r}")
assert menu_after["lock_msg_shown"] is False, "장착 뒤에도 잠금 안내가 보입니다"
assert prepare_url.endswith("/battle/prepare"), \
    f"전투 준비 화면 주소: 기대 /battle/prepare, 실제 {prepare_url}"

# TC-9-04. 한 칸만 골랐을 때는 합이 그 영웅의 전투력이고 출전은 비활성입니다
assert one_pick_state == {"sum": str(power_sum(ONE_PICK)),
                          "btn_enabled": False,
                          "msg": MSG_NOT_FULL}, f"한 칸만 고른 상태: 실제 {one_pick_state}"

# TC-9-05. 같은 영웅을 두 번 골라 3칸이 차도 출전은 비활성입니다
assert duplicated_state == {"sum": str(power_sum(DUPLICATED_PICK)),
                            "btn_enabled": False,
                            "msg": MSG_DUPLICATED}, f"같은 영웅 두 번 고른 상태: 실제 {duplicated_state}"

# TC-9-06 · TC-9-07. 3칸이 서로 다르면 출전이 활성되고 안내는 비워집니다.
# 활성 조건을 어긴 파티와 지킨 파티를 같은 모양으로 비교해 조건 3가지가 모두 확인됩니다
lose_sum = power_sum(LOSE_PICK)
win_sum = power_sum(WIN_PICK)
assert lose_party_state == {"sum": str(lose_sum), "btn_enabled": True, "msg": ""}, \
    f"패배 파티 상태: 실제 {lose_party_state}"
assert win_party_state == {"sum": str(win_sum), "btn_enabled": True, "msg": ""}, \
    f"승리 파티 상태: 실제 {win_party_state}"

# 승패 기대 문구는 기획서 영웅 표의 전투력을 더해 먼저 만듭니다
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

# 매칭은 5초가 걸립니다.
# 초를 세어 두는 대신 결과를 기다리고, 걸린 시간이 5초 이상인지로 확인합니다
assert lose_result["elapsed"] >= MATCH_SECONDS and win_result["elapsed"] >= MATCH_SECONDS, \
    (f"매칭 대기: 기대 {MATCH_SECONDS}초 이상, "
     f"실제 패배 {lose_result['elapsed']}초·승리 {win_result['elapsed']}초")

# TC-9-08. 패배는 점수를 올리지 않으므로 승리 1회분만 오릅니다
assert my_rank_text == f"내 점수 {WIN_SCORE} · 순위 밖", f"내 순위 문구: 실제 {my_rank_text!r}"

# 없는 파일만 모아 개수로 판정하면 어느 스크린샷이 없는지 메시지에 남습니다
import os
missing_shots = [path for path in [shot_locked, shot_win] if not os.path.exists(path)]
assert len(missing_shots) == 0, f"스크린샷이 없습니다: {missing_shots}"

print("게임 실습 9 정답 통과")
