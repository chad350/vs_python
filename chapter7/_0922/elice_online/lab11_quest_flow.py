"""실습 11. 퀘스트 한 건을 처음부터 끝까지 · 정답 코드와 해설

화면 /quests        테스트 케이스 8개 (TC-11-01 ~ TC-11-08)

이 실습이 확인하는 것은 3가지입니다.
  ① 상태가 바뀔 때마다 버튼 5가지의 활성 여부를 기획서 규칙 표와 비교하는가
  ② 결과 문구를 남기지 않는 진행 버튼을 진행도 글자 변화로 기다리는가
  ③ 완료 보상 기대값을 화면 표시가 아니라 기획서 보상 표에서 계산하는가

이 문항은 AssertionError 로 끝나는 것이 정답입니다 (종료 코드 1).
완료 보상이 기획서와 다르게 지급되며, 완료 전·완료 뒤 골드와 결과 문구를 한 메시지로 보고합니다.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from game_login import setup, make_wait, close_dialog, save_screenshot, GAME_URL

# ── 기획 데이터 (화면에서 읽지 않고 기획서 값을 코드에 적습니다)
SPEC_QUESTS = [("q1", "약초 채집", 5, 150), ("q2", "늑대 사냥", 3, 200),
               ("q3", "광석 운반", 2, 120), ("q4", "보급품 정리", 4, 180)]
START_GOLD = 1000
TARGET = "q1"                   # 수락부터 완료까지 지나가는 퀘스트입니다
DROP_TARGET = "q2"              # 수락·진행·포기까지만 해 보는 퀘스트입니다
MEMO_TEXT = "약초는 서쪽 언덕"

# 퀘스트 번호로 이름 · 목표 횟수 · 보상 골드를 바로 찾을 수 있게 딕셔너리 3개를 만들어 둡니다.
# 목록을 그때그때 뒤지면 같은 검색이 여러 곳에 흩어집니다
NAME = {}
GOAL = {}
REWARD = {}
for quest_id, quest_name, goal, reward in SPEC_QUESTS:
    NAME[quest_id] = quest_name
    GOAL[quest_id] = goal
    REWARD[quest_id] = reward

# 상태별로 (수락 · 진행 · 완료 · 포기 · 메모 저장) 5가지 버튼의 활성 여부입니다
BUTTON_RULES = {"수락 전": (True, False, False, False, False),
                "진행 중": (False, True, False, True, True),
                "완료 가능": (False, False, True, True, True),
                "완료": (False, False, False, False, True)}


def step(title):
    """진행 단계를 출력합니다.

    어느 단계의 값인지 출력에서 구분하기 위해서입니다.
    """
    print(f"\n=== {title} ===")


def to_int(text):
    """화면 글자를 정수로 바꿉니다.

    화면 값은 1,000 처럼 쉼표가 들어 있어 그대로 int() 에 넣으면 ValueError 가 발생합니다.
    """
    return int(text.replace(",", "").strip())


def read_gold(driver):
    """퀘스트 화면의 보유 골드를 정수로 읽습니다 (TC-11-02)."""
    el_gold = driver.find_element(By.ID, "quest-gold")
    return to_int(el_gold.text)


def read_card(driver, quest_id):
    """카드 1장의 상태 · 진행도 · 보상 표시 · 버튼 활성 여부를 딕셔너리로 모읍니다.

    버튼 5가지를 튜플로 모으면 기획서 규칙 표와 == 한 번으로 비교할 수 있습니다.
    메모 저장은 자주 확인하므로 튜플 안에 두면서 따로도 남깁니다.
    """
    el_state = driver.find_element(By.ID, f"q-state-{quest_id}")
    el_progress = driver.find_element(By.ID, f"q-progress-{quest_id}")
    el_reward = driver.find_element(By.ID, f"q-reward-{quest_id}")
    el_accept_btn = driver.find_element(By.ID, f"q-accept-{quest_id}")
    el_step_btn = driver.find_element(By.ID, f"q-step-{quest_id}")
    el_done_btn = driver.find_element(By.ID, f"q-done-{quest_id}")
    el_drop_btn = driver.find_element(By.ID, f"q-drop-{quest_id}")
    el_memo_save_btn = driver.find_element(By.ID, f"q-memo-save-{quest_id}")

    memo_save_enabled = el_memo_save_btn.is_enabled()
    return {"state": el_state.text,
            "progress": el_progress.text,
            "reward": el_reward.text,
            "buttons": (el_accept_btn.is_enabled(),
                        el_step_btn.is_enabled(),
                        el_done_btn.is_enabled(),
                        el_drop_btn.is_enabled(),
                        memo_save_enabled),
            "memo_save": memo_save_enabled}


def open_quests(driver, wait):
    """퀘스트 화면을 열고 카드 4장이 만들어질 때까지 기다립니다.

    빈 목록을 읽으면 카드가 없다고 확인하게 됩니다.
    """
    driver.get(GAME_URL + "/quests")
    # wait.until 은 조건을 0.5초 간격으로 다시 실행해 참이 될 때까지 기다립니다.
    # 그래서 인자로 「값」 이 아니라 「호출할 함수」 를 전달해야 합니다.
    #   len(driver.find_elements(...)) == 4      ← 지금 시점에서 한 번 계산한 True/False 입니다
    #   lambda d: len(d.find_elements(...)) == 4 ← 회차마다 다시 세는 함수입니다
    # lambda 는 이름 없는 함수라 def 로 따로 정의하지 않고 조건 1개를 그대로 작성할 수 있고,
    # 매개변수 d 에는 wait 를 만들 때 지정한 driver 가 회차마다 전달됩니다
    wait.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, "#quest-list .quest-card")) == len(SPEC_QUESTS),
               message="퀘스트 카드 4장이 표시되지 않음")


def click_and_wait_state(driver, wait, button_id, quest_id, expected_state, expected_msg_part):
    """버튼을 누르고 결과 문구와 상태 글자를 차례로 기다린 뒤 결과 문구를 반환합니다.

    결과 문구만 보고 카드를 읽으면 다시 만들기 전 상태를 읽습니다.
    상태 글자까지 기다려야 카드가 새로 만들어진 뒤의 값을 읽습니다.
    """
    el_button = driver.find_element(By.ID, button_id)
    el_button.click()
    wait.until(EC.text_to_be_present_in_element((By.ID, "quest-msg"), expected_msg_part),
               message=f"결과 문구에 {expected_msg_part!r} 가 나오지 않음")

    el_msg = driver.find_element(By.ID, "quest-msg")
    msg = el_msg.text
    wait.until(EC.text_to_be_present_in_element((By.ID, f"q-state-{quest_id}"), expected_state),
               message=f"상태가 {expected_state} 으로 바뀌지 않음")
    return msg


# =====================================================================
# 진행
# =====================================================================
driver, _ = setup()
wait = make_wait(driver, 10)

# ── TC-11-01 · TC-11-02. 처음 상태와 보유 골드
step("퀘스트 4건의 처음 상태")
open_quests(driver, wait)
first_cards = {}

for quest_id, quest_name, _goal, _reward in SPEC_QUESTS:
    first_cards[quest_id] = read_card(driver, quest_id)
    print(f" {quest_id} {quest_name} {first_cards[quest_id]}")

start_gold = read_gold(driver)
print("보유 골드:", start_gold)

# ── TC-11-03. 수락
step(f"{NAME[TARGET]} 수락")
accept_msg = click_and_wait_state(driver, wait, f"q-accept-{TARGET}", TARGET,
                                  "진행 중", f"퀘스트 수락: {NAME[TARGET]}")
accepted_state = read_card(driver, TARGET)
print(f"{accept_msg} {accepted_state}")

# ── TC-11-04. 목표 횟수만큼 진행
step(f"{NAME[TARGET]} 진행 {GOAL[TARGET]}회")
turn_states = []                    # 회차별 카드 상태입니다 (규칙 표와 한꺼번에 비교합니다)

for turn in range(1, GOAL[TARGET] + 1):
    el_step_btn = driver.find_element(By.ID, f"q-step-{TARGET}")
    el_step_btn.click()
    # 진행 버튼은 결과 문구를 남기지 않습니다.
    # 진행도 글자가 바뀌는 것을 신호로 삼지 않으면 앞 회차의 진행도를 읽습니다
    wait.until(EC.text_to_be_present_in_element((By.ID, f"q-progress-{TARGET}"),
                                                f"{turn} / {GOAL[TARGET]}"),
               message=f"진행 {turn}회 뒤 진행도가 바뀌지 않음")

    values = read_card(driver, TARGET)
    turn_states.append(values)
    print(f" {turn}회: 상태 {values['state']} · 진행 {values['progress']}")

# ── TC-11-05. 메모 저장과 새로고침
step("메모 저장과 새로고침")
el_memo = driver.find_element(By.ID, f"q-memo-{TARGET}")
el_memo.clear()                     # 지우지 않으면 앞 메모 뒤에 붙어 다른 글자가 저장됩니다
el_memo.send_keys(MEMO_TEXT)
memo_msg = click_and_wait_state(driver, wait, f"q-memo-save-{TARGET}", TARGET,
                                "완료 가능", "메모 저장 완료")

open_quests(driver, wait)
el_memo = driver.find_element(By.ID, f"q-memo-{TARGET}")
memo_after_reload = el_memo.get_attribute("value")
print(f"{memo_msg} · 새로고침 뒤 메모 {memo_after_reload!r}")

# ── TC-11-06 · TC-11-08. 완료 전 값을 먼저 읽어 둡니다
step("완료 전 보유 골드")
gold_before_done = read_gold(driver)
before_done_state = read_card(driver, TARGET)
print(f"보유 골드 {gold_before_done} · 카드 보상 표시 {before_done_state['reward']}G"
      f" · 상태 {before_done_state['state']}")

step(f"{NAME[TARGET]} 완료")
el_done_btn = driver.find_element(By.ID, f"q-done-{TARGET}")
el_done_btn.click()
# Dialog 를 닫지 않고 다음 버튼을 누르면 ElementClickInterceptedException 이 발생합니다
close_dialog(driver, wait)
wait.until(EC.text_to_be_present_in_element((By.ID, "quest-msg"), "퀘스트 완료"),
           message="완료 결과 문구가 나오지 않음")

el_msg = driver.find_element(By.ID, "quest-msg")
done_msg = el_msg.text
wait.until(EC.text_to_be_present_in_element((By.ID, f"q-state-{TARGET}"), "완료"),
           message="상태가 완료로 바뀌지 않음")

done_state = read_card(driver, TARGET)
gold_after_done = read_gold(driver)
el_target_card = driver.find_element(By.ID, f"quest-card-{TARGET}")
shot_done = save_screenshot(driver, "11_약초채집_완료_뒤", el_target_card)

# 기대 골드는 화면 표시가 아니라 기획서 보상 표에서 계산합니다.
# 화면 값으로 기대를 만들면 보상이 잘못 지급되어도 그대로 통과합니다
expected_reward = REWARD[TARGET]
expected_gold = gold_before_done + expected_reward
print(done_msg)
print(f"완료 뒤 보유 골드 {gold_after_done} · 기획서 보상 표로 계산한 기대 {expected_gold}"
      f" · 실제로 오른 골드 {gold_after_done - gold_before_done}")
print(f"완료 뒤 카드: {done_state}")

# ── TC-11-07. 다른 퀘스트로 포기까지
step(f"{NAME[DROP_TARGET]} 수락 · 진행 1회 · 포기")
click_and_wait_state(driver, wait, f"q-accept-{DROP_TARGET}", DROP_TARGET,
                     "진행 중", f"퀘스트 수락: {NAME[DROP_TARGET]}")
el_step_btn = driver.find_element(By.ID, f"q-step-{DROP_TARGET}")
el_step_btn.click()
wait.until(EC.text_to_be_present_in_element((By.ID, f"q-progress-{DROP_TARGET}"),
                                            f"1 / {GOAL[DROP_TARGET]}"),
           message="진행도가 1 로 바뀌지 않음")

state_before_drop = read_card(driver, DROP_TARGET)
print(f"포기 전 {state_before_drop}")

drop_msg = click_and_wait_state(driver, wait, f"q-drop-{DROP_TARGET}", DROP_TARGET,
                                "수락 전", f"퀘스트 포기: {NAME[DROP_TARGET]}")
state_after_drop = read_card(driver, DROP_TARGET)
print(f"{drop_msg} · 포기 뒤 {state_after_drop}")

driver.quit()


# =====================================================================
# 검증 (브라우저를 닫은 뒤 모아 둔 값을 한꺼번에 비교합니다)
# =====================================================================
# TC-11-01. 4건 모두 수락 전이고 수락 버튼만 활성입니다.
# 규칙과 다른 퀘스트만 모아 개수로 판정하면 어느 퀘스트가 달랐는지 메시지에 남습니다
wrong_first = [quest_id for quest_id in first_cards
               if first_cards[quest_id] != {"state": "수락 전",
                                            "progress": f"0 / {GOAL[quest_id]}",
                                            "reward": str(REWARD[quest_id]),
                                            "buttons": BUTTON_RULES["수락 전"],
                                            "memo_save": False}]
assert len(wrong_first) == 0, f"처음 상태가 기획서와 다른 퀘스트: {wrong_first} · {first_cards}"

# TC-11-02. 처음 보유 골드는 데이터 초기화 직후 값입니다
assert start_gold == START_GOLD, f"처음 보유 골드: 기대 {START_GOLD}, 실제 {start_gold}"

# TC-11-03. 수락하면 진행·포기·메모가 활성이 되고 수락은 비활성이 됩니다
assert accept_msg == f"퀘스트 수락: {NAME[TARGET]}", f"수락 결과 문구: 실제 {accept_msg!r}"
assert accepted_state["buttons"] == BUTTON_RULES["진행 중"], \
    f"수락 뒤 버튼 활성: 기대 {BUTTON_RULES['진행 중']}, 실제 {accepted_state['buttons']}"

# TC-11-04. 회차마다 진행도가 1 오르고, 목표 횟수에 닿으면 완료 가능이 됩니다
for turn in range(1, GOAL[TARGET] + 1):
    values = turn_states[turn - 1]
    assert values["progress"] == f"{turn} / {GOAL[TARGET]}", \
        f"진행 {turn}회 뒤 진행도: 기대 '{turn} / {GOAL[TARGET]}', 실제 {values['progress']!r}"

    expected_state = "완료 가능" if turn == GOAL[TARGET] else "진행 중"
    assert values["state"] == expected_state, \
        f"진행 {turn}회 뒤 상태: 기대 {expected_state!r}, 실제 {values['state']!r}"
    assert values["buttons"] == BUTTON_RULES[expected_state], \
        (f"진행 {turn}회 뒤 버튼 활성: 기대 {BUTTON_RULES[expected_state]}, "
         f"실제 {values['buttons']}")

# TC-11-05. 메모는 화면을 다시 열어도 남아 있습니다
assert memo_msg == "메모 저장 완료", f"메모 저장 결과 문구: 실제 {memo_msg!r}"
assert memo_after_reload == MEMO_TEXT, \
    f"새로고침 뒤 메모: 기대 {MEMO_TEXT!r}, 실제 {memo_after_reload!r}"

# TC-11-06. 완료하면 메모만 활성이고 카드 보상 표시는 기획서 값 그대로입니다
assert done_state["state"] == "완료", f"완료 뒤 상태: 기대 '완료', 실제 {done_state['state']!r}"
assert done_state["buttons"] == BUTTON_RULES["완료"], \
    f"완료 뒤 버튼 활성: 기대 {BUTTON_RULES['완료']}, 실제 {done_state['buttons']}"
assert done_state["reward"] == str(expected_reward), \
    f"완료 뒤 카드 보상 표시: 기대 {expected_reward}, 실제 {done_state['reward']!r}"

# TC-11-07. 포기 뒤에는 상태 글자만이 아니라 진행도와 버튼까지 되돌아갑니다
assert drop_msg == f"퀘스트 포기: {NAME[DROP_TARGET]}", f"포기 결과 문구: 실제 {drop_msg!r}"
assert (state_after_drop["state"],
        state_after_drop["progress"],
        state_after_drop["buttons"]) == ("수락 전",
                                         f"0 / {GOAL[DROP_TARGET]}",
                                         BUTTON_RULES["수락 전"]), \
    (f"포기 뒤: 기대 상태 '수락 전'·진행도 '0 / {GOAL[DROP_TARGET]}'"
     f"·버튼 {BUTTON_RULES['수락 전']}, 실제 {state_after_drop['state']!r}"
     f"·{state_after_drop['progress']!r}·{state_after_drop['buttons']}")

# 없는 파일만 모아 개수로 판정하면 어느 스크린샷이 없는지 메시지에 남습니다
import os
missing_shots = [path for path in [shot_done] if not os.path.exists(path)]
assert len(missing_shots) == 0, f"스크린샷이 없습니다: {missing_shots}"

# TC-11-08. 보상 비교를 마지막에 두어, 다른 규칙을 모두 확인한 뒤 보고합니다.
# 기대값을 화면 표시로 바꾸면 보상이 잘못 지급되어도 통과하므로 기획서 값을 그대로 둡니다
assert (gold_after_done, done_msg) == (expected_gold,
                                       f"퀘스트 완료: {NAME[TARGET]} · 보상 {expected_reward}G"), \
    (f"{NAME[TARGET]} 완료 보상: 기대 골드 {gold_before_done} → {expected_gold}"
     f"(보상 {expected_reward}G), 실제 골드 {gold_before_done} → {gold_after_done}"
     f"(오른 골드 {gold_after_done - gold_before_done}). "
     f"결과 문구: 기대 '퀘스트 완료: {NAME[TARGET]} · 보상 {expected_reward}G', "
     f"실제 {done_msg!r}. "
     f"카드의 보상 표시는 {done_state['reward']}G 그대로입니다")
