"""실습 종합. 로그인 뒤 랭킹 확인까지 한 흐름 · 정답 코드와 해설

화면 전체        테스트 케이스 7개 (TC-종합-01 ~ TC-종합-07)

이 실습이 확인하는 것은 3가지입니다.
  ① 단계마다 바뀐 상태를 기다려 확인하고 다음 단계로 넘어가는가
  ② 기대와 실제를 기록에 모아 두고 마지막에 한 번만 보고하는가
  ③ 골드를 구매 직후 상점 화면이 아니라 마이페이지를 새로 열어 읽는가

단계마다 assert 하면 앞 단계에서 멈춰 뒤 단계를 확인하지 못합니다.
그래서 record() 로 20단계를 모아 두고, 어긋난 단계만 마지막에 한 번 보고합니다.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from game_login import setup, make_wait, close_dialog, save_screenshot, GAME_URL, NICKNAME

# ── 기획 데이터 (화면에서 읽지 않고 기획서 값을 코드에 적습니다)
START_GOLD = 1000
MAIN_TITLE = "모험가의 거점"

BOW_ID = 12                          # 기획서 상점 표의 item_id 입니다
BOW_NAME = "사냥꾼의 활"
BOW_PRICE = 260
BOW_POWER = 55
SHIELD_ID = 13
SHIELD_NAME = "수호자의 방패"
SHIELD_PRICE = 300
SHIELD_POWER = 45
SHOP_ROWS = 8                        # 기획서 상점 아이템 표의 행 수입니다

QUEST_ID = "q2"
QUEST_NAME = "늑대 사냥"
QUEST_GOAL = 3
QUEST_REWARD = 200

WIN_PICK = ["h1", "h4", "h2"]        # 루앤 40 · 세라 45 · 미르 35
HERO_POWER = {"h1": 40, "h2": 35, "h3": 25, "h4": 45, "h5": 30}
NEED_POWER = 100
WIN_SCORE = 1000

# 기획서 값으로 단계별 기대 골드를 미리 계산해 둡니다.
# 화면 표시를 기대값으로 쓰면 골드가 잘못 줄어도 그대로 통과합니다
GOLD_AFTER_BUY = START_GOLD - BOW_PRICE - SHIELD_PRICE          # 1000 - 560 = 440
GOLD_AFTER_QUEST = GOLD_AFTER_BUY + QUEST_REWARD                # 440 + 200 = 640
EQUIP_POWER = BOW_POWER + SHIELD_POWER                          # 55 + 45 = 100
WIN_SUM = sum([HERO_POWER[hero_id] for hero_id in WIN_PICK])    # 40 + 45 + 35 = 120
EXPECTED_STEPS = 20                                             # 기록에 모으는 단계 수입니다

log = []                             # (단계 이름, 기대값, 실제값) 을 모아 두는 기록입니다


def step(title):
    """진행 단계를 출력합니다.

    어느 단계의 값인지 출력에서 구분하기 위해서입니다.
    """
    print(f"\n=== {title} ===")


def record(name, expected, actual):
    """한 단계의 기대값과 실제값을 기록에 모으고 바로 출력합니다.

    여기에서 바로 assert 하면 앞 단계에서 멈춰 뒤 단계를 확인하지 못합니다.
    기록에 모아 두면 흐름을 끝까지 지나간 뒤 어긋난 단계만 골라 보고할 수 있습니다.
    """
    log.append((name, expected, actual))
    print(f" {name}: 기대 {expected!r} · 실제 {actual!r}")


def to_int(text):
    """화면 글자를 정수로 바꿉니다.

    마이페이지 골드는 1,000 처럼 쉼표가 들어 있어 그대로 int() 에 넣으면 ValueError 가 발생합니다.
    """
    return int(text.replace(",", "").strip())


def me_gold(driver, wait):
    """마이페이지를 새로 열어 보유 골드를 읽습니다.

    구매 직후 상점 화면의 골드 표시는 이 흐름의 판정에 쓰지 않습니다.
    화면을 새로 열어 읽는 함수를 하나 두고 단계마다 부릅니다.
    """
    driver.get(GAME_URL + "/me")
    # wait.until 은 조건을 0.5초 간격으로 다시 실행해 참이 될 때까지 기다립니다.
    # 그래서 인자로 「값」 이 아니라 「호출할 함수」 를 전달해야 합니다.
    #   d.find_element(...).text != ""      ← 지금 시점에서 한 번 계산한 True/False 입니다
    #   lambda d: d.find_element(...).text != ""  ← 회차마다 다시 계산하는 함수입니다
    # lambda 는 이름 없는 함수라 def 로 따로 정의하지 않고 조건 1개를 그대로 작성할 수 있고,
    # 매개변수 d 에는 wait 를 만들 때 지정한 driver 가 회차마다 전달됩니다
    wait.until(lambda d: d.find_element(By.ID, "me-gold").text != "",
               message="마이페이지 골드가 표시되지 않음")

    el_gold = driver.find_element(By.ID, "me-gold")
    return to_int(el_gold.text)


def battle_menu_aria(driver):
    """전투 준비 메뉴의 aria-disabled 값을 읽습니다.

    잠김과 열림의 글자 색이 같으므로 색으로는 두 상태를 가려낼 수 없습니다.
    """
    el_menu = driver.find_element(By.ID, "menu-battle")
    return el_menu.get_attribute("aria-disabled")


def buy(driver, wait, item_id, item_name):
    """아이템 하나를 사고 결과 문구를 기록에 모은 뒤 Dialog 를 닫습니다."""
    el_buy_btn = wait.until(EC.element_to_be_clickable((By.ID, f"buy-btn-{item_id}")),
                            message=f"{item_name} 구매 버튼이 준비되지 않음")
    el_buy_btn.click()
    wait.until(EC.text_to_be_present_in_element((By.ID, "shop-msg"), f"구매 완료: {item_name}"),
               message=f"{item_name} 구매 결과 문구가 나오지 않음")

    el_shop_msg = driver.find_element(By.ID, "shop-msg")
    record(f"{item_name} 구매 문구", f"구매 완료: {item_name} x1", el_shop_msg.text)
    # 아이템마다 Dialog 가 열립니다.
    # 닫지 않으면 다음 구매 버튼에서 ElementClickInterceptedException 이 발생합니다
    close_dialog(driver, wait)


def equip(driver, wait, item_name, summary_id):
    """표의 장착 버튼을 눌러 장착하고 장착 요약이 바뀔 때까지 기다립니다."""
    el_row = driver.find_element(
        By.XPATH,
        f"//table[@id='inv-table']/tbody/tr[td[@class='col-name'][normalize-space()='{item_name}']]")
    # 가방 칸과 장착 버튼에는 행 번호가 붙어 있습니다.
    # 표에서 data-row-id 를 먼저 얻어 버튼 id 를 만듭니다
    row_id = el_row.get_attribute("data-row-id")
    el_equip_btn = driver.find_element(By.ID, f"eq-btn-{row_id}")
    el_equip_btn.click()
    wait.until(EC.text_to_be_present_in_element((By.ID, summary_id), item_name),
               message=f"{item_name} 이 장착되지 않음")


# =====================================================================
# 진행
# =====================================================================
driver, _ = setup()
# 매칭 5초를 포함해 넉넉히 20초로 정한 Wait 를 사용합니다
wait = make_wait(driver, 20)

# ── TC-종합-01. 로그인 직후 상태
step("로그인 (제공 코드)")
wait.until(EC.text_to_be_present_in_element((By.ID, "main-title"), MAIN_TITLE),
           message="메인 화면이 열리지 않음")

el_main_title = driver.find_element(By.ID, "main-title")
el_hdr_nick = driver.find_element(By.ID, "hdr-nick")
record("메인 메뉴 제목", MAIN_TITLE, el_main_title.text)
record("머리글 닉네임", NICKNAME, el_hdr_nick.text)
record("무기 장착 전 전투 준비 메뉴", "true", battle_menu_aria(driver))
record("초기화 직후 마이페이지 골드", START_GOLD, me_gold(driver, wait))

# ── TC-종합-02. 상점에서 무기와 방어구 구매
step("상점 구매")
driver.get(GAME_URL + "/shop")
# 반쯤 만들어진 표를 읽으면 구매 버튼을 찾지 못합니다
wait.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, "#shop-table tbody tr")) == SHOP_ROWS,
           message="상점 표가 8행이 되지 않음")

buy(driver, wait, BOW_ID, BOW_NAME)
buy(driver, wait, SHIELD_ID, SHIELD_NAME)

# ── TC-종합-03. 구매 뒤 골드는 마이페이지에서 읽습니다
record("구매 뒤 마이페이지 골드", GOLD_AFTER_BUY, me_gold(driver, wait))

# ── TC-종합-04. 무기와 방어구 장착
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

# ── TC-종합-05. 퀘스트 수락 · 진행 · 완료
step("퀘스트 수락·진행·완료")
driver.get(GAME_URL + "/quests")
wait.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, "#quest-list .quest-card")) == 4,
           message="퀘스트 카드 4장이 표시되지 않음")

el_accept_btn = driver.find_element(By.ID, f"q-accept-{QUEST_ID}")
el_accept_btn.click()
# 결과 문구만 보고 카드를 읽으면 다시 만들기 전 상태를 읽습니다
wait.until(EC.text_to_be_present_in_element((By.ID, f"q-state-{QUEST_ID}"), "진행 중"),
           message="상태가 진행 중으로 바뀌지 않음")

for turn in range(1, QUEST_GOAL + 1):
    el_step_btn = driver.find_element(By.ID, f"q-step-{QUEST_ID}")
    el_step_btn.click()
    # 진행 버튼은 결과 문구를 남기지 않으므로 진행도 글자가 바뀌는 것을 신호로 삼습니다
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

# ── TC-종합-06. 전투 승리
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
    # select 는 click 과 send_keys 로 다루면 브라우저마다 다르게 움직입니다.
    # Select 로 값을 지정하면 change 가 함께 일어나 전투력 합이 다시 계산됩니다
    Select(el_slot).select_by_value(WIN_PICK[number - 1])

# 칸을 고친 직후에 버튼 상태를 읽으면 다시 계산되기 전 값을 읽습니다
wait.until(EC.text_to_be_present_in_element((By.ID, "party-power"), str(WIN_SUM)),
           message="전투력 합이 다시 계산되지 않음")

el_party_power = driver.find_element(By.ID, "party-power")
el_start_btn = driver.find_element(By.ID, "battle-start")
record("파티 전투력 합", str(WIN_SUM), el_party_power.text)
record("출전 버튼", True, el_start_btn.is_enabled())

el_start_btn.click()
# 5초를 세어 두면 화면이 늦을 때 값을 잘못 읽습니다.
# 결과 문구가 채워지는 것을 기다립니다
wait.until(lambda d: d.find_element(By.ID, "battle-result").text != "",
           message="전투 결과가 나오지 않음")

el_battle_state = driver.find_element(By.ID, "battle-state")
el_battle_result = driver.find_element(By.ID, "battle-result")
record("전투 상태", "매칭 완료", el_battle_state.text)
record("전투 결과 문구", f"승리 · 전투력 {WIN_SUM} / 요구 {NEED_POWER}", el_battle_result.text)
close_dialog(driver, wait)

# ── TC-종합-07. 랭킹에서 내 순위
step("랭킹 「내 순위」 확인")
driver.get(GAME_URL + "/ranking")
wait.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, "#rank-table tbody tr")) == 10,
           message="랭킹 표가 10행이 되지 않음")
# 내 순위 문구는 목록 응답이 온 뒤에 채워집니다
wait.until(lambda d: d.find_element(By.ID, "my-rank").text != "",
           message="내 순위 문구가 나오지 않음")

el_my_rank = driver.find_element(By.ID, "my-rank")
record("내 순위 문구", f"내 점수 {WIN_SCORE} · 순위 밖", el_my_rank.text)
shot_my_rank = save_screenshot(driver, "종합_내_순위", el_my_rank)

driver.quit()


# =====================================================================
# 검증 (브라우저를 닫은 뒤 모아 둔 기록을 한꺼번에 비교합니다)
# =====================================================================
print("\n단계별 기대값과 실제값")
for name, expected, actual in log:
    mark = "O" if expected == actual else "X"
    print(f" {mark} {name}: 기대 {expected!r} · 실제 {actual!r}")

# 기대와 다른 단계만 모아 개수로 판정하면 어느 단계가 어긋났는지 메시지에 남습니다
mismatched = [(name, expected, actual) for name, expected, actual in log if expected != actual]
assert len(mismatched) == 0, f"기획서와 다른 단계 {len(mismatched)}건: {mismatched}"

# 단계 수까지 확인해야 중간에서 빠뜨린 기록이 없는지 알 수 있습니다
assert len(log) == EXPECTED_STEPS, f"모은 단계 수: 기대 {EXPECTED_STEPS}, 실제 {len(log)}"

# 없는 파일만 모아 개수로 판정하면 어느 스크린샷이 없는지 메시지에 남습니다
import os
missing_shots = [path for path in [shot_my_rank] if not os.path.exists(path)]
assert len(missing_shots) == 0, f"스크린샷이 없습니다: {missing_shots}"

print("게임 실습 종합 정답 통과")
