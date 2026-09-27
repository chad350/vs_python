from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from game_login import setup, make_wait, close_dialog, save_screenshot, GAME_URL

SPEC_QUESTS = [("q1", "약초 채집", 5, 150), ("q2", "늑대 사냥", 3, 200),
               ("q3", "광석 운반", 2, 120), ("q4", "보급품 정리", 4, 180)]
START_GOLD = 1000
TARGET = "q1"
DROP_TARGET = "q2"
MEMO_TEXT = "약초는 서쪽 언덕"

NAME = {}
GOAL = {}
REWARD = {}
for quest_id, quest_name, goal, reward in SPEC_QUESTS:
    NAME[quest_id] = quest_name
    GOAL[quest_id] = goal
    REWARD[quest_id] = reward

BUTTON_RULES = {"수락 전": (True, False, False, False, False),
                "진행 중": (False, True, False, True, True),
                "완료 가능": (False, False, True, True, True),
                "완료": (False, False, False, False, True)}


def step(title):
    print(f"\n=== {title} ===")


def to_int(text):
    return int(text.replace(",", "").strip())


def read_gold(driver):
    el_gold = driver.find_element(By.ID, "quest-gold")
    return to_int(el_gold.text)


def read_card(driver, quest_id):
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
    driver.get(GAME_URL + "/quests")
    wait.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, "#quest-list .quest-card")) == len(SPEC_QUESTS),
               message="퀘스트 카드 4장이 표시되지 않음")


def click_and_wait_state(driver, wait, button_id, quest_id, expected_state, expected_msg_part):
    el_button = driver.find_element(By.ID, button_id)
    el_button.click()
    wait.until(EC.text_to_be_present_in_element((By.ID, "quest-msg"), expected_msg_part),
               message=f"결과 문구에 {expected_msg_part!r} 가 나오지 않음")

    el_msg = driver.find_element(By.ID, "quest-msg")
    msg = el_msg.text
    wait.until(EC.text_to_be_present_in_element((By.ID, f"q-state-{quest_id}"), expected_state),
               message=f"상태가 {expected_state} 으로 바뀌지 않음")
    return msg


driver, _ = setup()
wait = make_wait(driver, 10)

step("퀘스트 4건의 처음 상태")
open_quests(driver, wait)
first_cards = {}

for quest_id, quest_name, _goal, _reward in SPEC_QUESTS:
    first_cards[quest_id] = read_card(driver, quest_id)
    print(f" {quest_id} {quest_name} {first_cards[quest_id]}")

start_gold = read_gold(driver)
print("보유 골드:", start_gold)

step(f"{NAME[TARGET]} 수락")
accept_msg = click_and_wait_state(driver, wait, f"q-accept-{TARGET}", TARGET,
                                  "진행 중", f"퀘스트 수락: {NAME[TARGET]}")
accepted_state = read_card(driver, TARGET)
print(f"{accept_msg} {accepted_state}")

step(f"{NAME[TARGET]} 진행 {GOAL[TARGET]}회")
turn_states = []

for turn in range(1, GOAL[TARGET] + 1):
    el_step_btn = driver.find_element(By.ID, f"q-step-{TARGET}")
    el_step_btn.click()
    wait.until(EC.text_to_be_present_in_element((By.ID, f"q-progress-{TARGET}"),
                                                f"{turn} / {GOAL[TARGET]}"),
               message=f"진행 {turn}회 뒤 진행도가 바뀌지 않음")

    values = read_card(driver, TARGET)
    turn_states.append(values)
    print(f" {turn}회: 상태 {values['state']} · 진행 {values['progress']}")

step("메모 저장과 새로고침")
el_memo = driver.find_element(By.ID, f"q-memo-{TARGET}")
el_memo.clear()
el_memo.send_keys(MEMO_TEXT)
memo_msg = click_and_wait_state(driver, wait, f"q-memo-save-{TARGET}", TARGET,
                                "완료 가능", "메모 저장 완료")

open_quests(driver, wait)
el_memo = driver.find_element(By.ID, f"q-memo-{TARGET}")
memo_after_reload = el_memo.get_attribute("value")
print(f"{memo_msg} · 새로고침 뒤 메모 {memo_after_reload!r}")

step("완료 전 보유 골드")
gold_before_done = read_gold(driver)
before_done_state = read_card(driver, TARGET)
print(f"보유 골드 {gold_before_done} · 카드 보상 표시 {before_done_state['reward']}G"
      f" · 상태 {before_done_state['state']}")

step(f"{NAME[TARGET]} 완료")
el_done_btn = driver.find_element(By.ID, f"q-done-{TARGET}")
el_done_btn.click()
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

expected_reward = REWARD[TARGET]
expected_gold = gold_before_done + expected_reward
print(done_msg)
print(f"완료 뒤 보유 골드 {gold_after_done} · 기획서 보상 표로 계산한 기대 {expected_gold}"
      f" · 실제로 오른 골드 {gold_after_done - gold_before_done}")
print(f"완료 뒤 카드: {done_state}")

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


wrong_first = [quest_id for quest_id in first_cards
               if first_cards[quest_id] != {"state": "수락 전",
                                            "progress": f"0 / {GOAL[quest_id]}",
                                            "reward": str(REWARD[quest_id]),
                                            "buttons": BUTTON_RULES["수락 전"],
                                            "memo_save": False}]
assert len(wrong_first) == 0, f"처음 상태가 기획서와 다른 퀘스트: {wrong_first} · {first_cards}"

assert start_gold == START_GOLD, f"처음 보유 골드: 기대 {START_GOLD}, 실제 {start_gold}"

assert accept_msg == f"퀘스트 수락: {NAME[TARGET]}", f"수락 결과 문구: 실제 {accept_msg!r}"
assert accepted_state["buttons"] == BUTTON_RULES["진행 중"], \
    f"수락 뒤 버튼 활성: 기대 {BUTTON_RULES['진행 중']}, 실제 {accepted_state['buttons']}"

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

assert memo_msg == "메모 저장 완료", f"메모 저장 결과 문구: 실제 {memo_msg!r}"
assert memo_after_reload == MEMO_TEXT, \
    f"새로고침 뒤 메모: 기대 {MEMO_TEXT!r}, 실제 {memo_after_reload!r}"

assert done_state["state"] == "완료", f"완료 뒤 상태: 기대 '완료', 실제 {done_state['state']!r}"
assert done_state["buttons"] == BUTTON_RULES["완료"], \
    f"완료 뒤 버튼 활성: 기대 {BUTTON_RULES['완료']}, 실제 {done_state['buttons']}"
assert done_state["reward"] == str(expected_reward), \
    f"완료 뒤 카드 보상 표시: 기대 {expected_reward}, 실제 {done_state['reward']!r}"

assert drop_msg == f"퀘스트 포기: {NAME[DROP_TARGET]}", f"포기 결과 문구: 실제 {drop_msg!r}"
assert (state_after_drop["state"],
        state_after_drop["progress"],
        state_after_drop["buttons"]) == ("수락 전",
                                         f"0 / {GOAL[DROP_TARGET]}",
                                         BUTTON_RULES["수락 전"]), \
    (f"포기 뒤: 기대 상태 '수락 전'·진행도 '0 / {GOAL[DROP_TARGET]}'"
     f"·버튼 {BUTTON_RULES['수락 전']}, 실제 {state_after_drop['state']!r}"
     f"·{state_after_drop['progress']!r}·{state_after_drop['buttons']}")

import os
missing_shots = [path for path in [shot_done] if not os.path.exists(path)]
assert len(missing_shots) == 0, f"스크린샷이 없습니다: {missing_shots}"

assert (gold_after_done, done_msg) == (expected_gold,
                                       f"퀘스트 완료: {NAME[TARGET]} · 보상 {expected_reward}G"), \
    (f"{NAME[TARGET]} 완료 보상: 기대 골드 {gold_before_done} → {expected_gold}"
     f"(보상 {expected_reward}G), 실제 골드 {gold_before_done} → {gold_after_done}"
     f"(오른 골드 {gold_after_done - gold_before_done}). "
     f"결과 문구: 기대 '퀘스트 완료: {NAME[TARGET]} · 보상 {expected_reward}G', "
     f"실제 {done_msg!r}. "
     f"카드의 보상 표시는 {done_state['reward']}G 그대로입니다")
