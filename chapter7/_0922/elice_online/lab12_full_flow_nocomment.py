from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from game_login import setup, make_wait, close_dialog, save_screenshot, GAME_URL, NICKNAME

START_GOLD = 1000
MAIN_TITLE = "모험가의 거점"

BOW_ID = 12
BOW_NAME = "사냥꾼의 활"
BOW_PRICE = 260
BOW_POWER = 55
SHIELD_ID = 13
SHIELD_NAME = "수호자의 방패"
SHIELD_PRICE = 300
SHIELD_POWER = 45
SHOP_ROWS = 8

QUEST_ID = "q2"
QUEST_NAME = "늑대 사냥"
QUEST_GOAL = 3
QUEST_REWARD = 200

WIN_PICK = ["h1", "h4", "h2"]
HERO_POWER = {"h1": 40, "h2": 35, "h3": 25, "h4": 45, "h5": 30}
NEED_POWER = 100
WIN_SCORE = 1000

GOLD_AFTER_BUY = START_GOLD - BOW_PRICE - SHIELD_PRICE
GOLD_AFTER_QUEST = GOLD_AFTER_BUY + QUEST_REWARD
EQUIP_POWER = BOW_POWER + SHIELD_POWER
WIN_SUM = sum([HERO_POWER[hero_id] for hero_id in WIN_PICK])
EXPECTED_STEPS = 20

log = []


def step(title):
    print(f"\n=== {title} ===")


def record(name, expected, actual):
    log.append((name, expected, actual))
    print(f" {name}: 기대 {expected!r} · 실제 {actual!r}")


def to_int(text):
    return int(text.replace(",", "").strip())


def me_gold(driver, wait):
    driver.get(GAME_URL + "/me")
    wait.until(lambda d: d.find_element(By.ID, "me-gold").text != "",
               message="마이페이지 골드가 표시되지 않음")

    el_gold = driver.find_element(By.ID, "me-gold")
    return to_int(el_gold.text)


def battle_menu_aria(driver):
    el_menu = driver.find_element(By.ID, "menu-battle")
    return el_menu.get_attribute("aria-disabled")


def buy(driver, wait, item_id, item_name):
    el_buy_btn = wait.until(EC.element_to_be_clickable((By.ID, f"buy-btn-{item_id}")),
                            message=f"{item_name} 구매 버튼이 준비되지 않음")
    el_buy_btn.click()
    wait.until(EC.text_to_be_present_in_element((By.ID, "shop-msg"), f"구매 완료: {item_name}"),
               message=f"{item_name} 구매 결과 문구가 나오지 않음")

    el_shop_msg = driver.find_element(By.ID, "shop-msg")
    record(f"{item_name} 구매 문구", f"구매 완료: {item_name} x1", el_shop_msg.text)
    close_dialog(driver, wait)


def equip(driver, wait, item_name, summary_id):
    el_row = driver.find_element(
        By.XPATH,
        f"//table[@id='inv-table']/tbody/tr[td[@class='col-name'][normalize-space()='{item_name}']]")
    row_id = el_row.get_attribute("data-row-id")
    el_equip_btn = driver.find_element(By.ID, f"eq-btn-{row_id}")
    el_equip_btn.click()
    wait.until(EC.text_to_be_present_in_element((By.ID, summary_id), item_name),
               message=f"{item_name} 이 장착되지 않음")


driver, _ = setup()
wait = make_wait(driver, 20)

step("로그인 (제공 코드)")
wait.until(EC.text_to_be_present_in_element((By.ID, "main-title"), MAIN_TITLE),
           message="메인 화면이 열리지 않음")

el_main_title = driver.find_element(By.ID, "main-title")
el_hdr_nick = driver.find_element(By.ID, "hdr-nick")
record("메인 메뉴 제목", MAIN_TITLE, el_main_title.text)
record("머리글 닉네임", NICKNAME, el_hdr_nick.text)
record("무기 장착 전 전투 준비 메뉴", "true", battle_menu_aria(driver))
record("초기화 직후 마이페이지 골드", START_GOLD, me_gold(driver, wait))

step("상점 구매")
driver.get(GAME_URL + "/shop")
wait.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, "#shop-table tbody tr")) == SHOP_ROWS,
           message="상점 표가 8행이 되지 않음")

buy(driver, wait, BOW_ID, BOW_NAME)
buy(driver, wait, SHIELD_ID, SHIELD_NAME)

record("구매 뒤 마이페이지 골드", GOLD_AFTER_BUY, me_gold(driver, wait))

step("장비 장착")
driver.get(GAME_URL + "/inventory")
wait.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, "#inv-table tbody tr")) == 2,
           message="인벤토리 표가 2행이 되지 않음")

equip(driver, wait, BOW_NAME, "equip-weapon")
equip(driver, wait, SHIELD_NAME, "equip-armor")

el_equip_weapon = driver.find_element(By.ID, "equip-weapon")
el_equip_armor = driver.find_element(By.ID, "equip-armor")
el_equip_power = driver.find_element(By.ID, "equip-power")
record("장착 무기", BOW_NAME, el_equip_weapon.text)
record("장착 방어구", SHIELD_NAME, el_equip_armor.text)
record("장착 전투력 합계", str(EQUIP_POWER), el_equip_power.text)

step("퀘스트 수락·진행·완료")
driver.get(GAME_URL + "/quests")
wait.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, "#quest-list .quest-card")) == 4,
           message="퀘스트 카드 4장이 표시되지 않음")

el_accept_btn = driver.find_element(By.ID, f"q-accept-{QUEST_ID}")
el_accept_btn.click()
wait.until(EC.text_to_be_present_in_element((By.ID, f"q-state-{QUEST_ID}"), "진행 중"),
           message="상태가 진행 중으로 바뀌지 않음")

for turn in range(1, QUEST_GOAL + 1):
    el_step_btn = driver.find_element(By.ID, f"q-step-{QUEST_ID}")
    el_step_btn.click()
    wait.until(EC.text_to_be_present_in_element((By.ID, f"q-progress-{QUEST_ID}"),
                                                f"{turn} / {QUEST_GOAL}"),
               message=f"진행 {turn}회 뒤 진행도가 바뀌지 않음")

el_quest_state = driver.find_element(By.ID, f"q-state-{QUEST_ID}")
record("진행을 다 채운 뒤 상태", "완료 가능", el_quest_state.text)

el_done_btn = driver.find_element(By.ID, f"q-done-{QUEST_ID}")
el_done_btn.click()
close_dialog(driver, wait)
wait.until(EC.text_to_be_present_in_element((By.ID, "quest-msg"), "퀘스트 완료"),
           message="완료 결과 문구가 나오지 않음")

el_quest_msg = driver.find_element(By.ID, "quest-msg")
record("완료 결과 문구", f"퀘스트 완료: {QUEST_NAME} · 보상 {QUEST_REWARD}G", el_quest_msg.text)
wait.until(EC.text_to_be_present_in_element((By.ID, f"q-state-{QUEST_ID}"), "완료"),
           message="상태가 완료로 바뀌지 않음")

el_quest_state = driver.find_element(By.ID, f"q-state-{QUEST_ID}")
record("완료 뒤 상태", "완료", el_quest_state.text)
record("퀘스트 보상 뒤 마이페이지 골드", GOLD_AFTER_QUEST, me_gold(driver, wait))

step("전투 승리")
driver.get(GAME_URL + "/main")
wait.until(EC.text_to_be_present_in_element((By.ID, "main-title"), MAIN_TITLE),
           message="메인 화면이 열리지 않음")
record("무기 장착 뒤 전투 준비 메뉴", "false", battle_menu_aria(driver))

driver.get(GAME_URL + "/battle/prepare")
wait.until(EC.presence_of_element_located((By.ID, "battle-start")),
           message="전투 준비 화면이 열리지 않음")

for number in [1, 2, 3]:
    el_slot = driver.find_element(By.ID, f"party-slot-{number}")
    Select(el_slot).select_by_value(WIN_PICK[number - 1])

wait.until(EC.text_to_be_present_in_element((By.ID, "party-power"), str(WIN_SUM)),
           message="전투력 합이 다시 계산되지 않음")

el_party_power = driver.find_element(By.ID, "party-power")
el_start_btn = driver.find_element(By.ID, "battle-start")
record("파티 전투력 합", str(WIN_SUM), el_party_power.text)
record("출전 버튼", True, el_start_btn.is_enabled())

el_start_btn.click()
wait.until(lambda d: d.find_element(By.ID, "battle-result").text != "",
           message="전투 결과가 나오지 않음")

el_battle_state = driver.find_element(By.ID, "battle-state")
el_battle_result = driver.find_element(By.ID, "battle-result")
record("전투 상태", "매칭 완료", el_battle_state.text)
record("전투 결과 문구", f"승리 · 전투력 {WIN_SUM} / 요구 {NEED_POWER}", el_battle_result.text)
close_dialog(driver, wait)

step("랭킹 「내 순위」 확인")
driver.get(GAME_URL + "/ranking")
wait.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, "#rank-table tbody tr")) == 10,
           message="랭킹 표가 10행이 되지 않음")
wait.until(lambda d: d.find_element(By.ID, "my-rank").text != "",
           message="내 순위 문구가 나오지 않음")

el_my_rank = driver.find_element(By.ID, "my-rank")
record("내 순위 문구", f"내 점수 {WIN_SCORE} · 순위 밖", el_my_rank.text)
shot_my_rank = save_screenshot(driver, "종합_내_순위", el_my_rank)

driver.quit()


print("\n단계별 기대값과 실제값")
for name, expected, actual in log:
    mark = "O" if expected == actual else "X"
    print(f" {mark} {name}: 기대 {expected!r} · 실제 {actual!r}")

mismatched = [(name, expected, actual) for name, expected, actual in log if expected != actual]
assert len(mismatched) == 0, f"기획서와 다른 단계 {len(mismatched)}건: {mismatched}"

assert len(log) == EXPECTED_STEPS, f"모은 단계 수: 기대 {EXPECTED_STEPS}, 실제 {len(log)}"

import os
missing_shots = [path for path in [shot_my_rank] if not os.path.exists(path)]
assert len(missing_shots) == 0, f"스크린샷이 없습니다: {missing_shots}"

print("게임 실습 종합 정답 통과")
