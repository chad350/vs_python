import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from game_login import setup, make_wait, save_screenshot, GAME_URL

TARGET_STREAK = 7
MAX_TRIES = 20
RUBY_REWARD = 50
SUCCESS_PREFIX = "출석 완료"
FAIL_MSG = "일시적인 오류로 출석 처리에 실패했습니다 (E503)"
REWARD_DONE = "보상 수령 완료"
MAX_FAIL_ALLOWED = 5
EXPECTED_TRIES = 8
EXPECTED_FAIL_TRIES = [5]
DAY7_CLASS = "day done"


def step(title):
    print(f"\n=== {title} ===")


def to_int(text):
    return int(text.replace(",", "").strip())


def read_status(driver):
    el_streak = driver.find_element(By.ID, "streak")
    el_ruby = driver.find_element(By.ID, "ruby")
    el_count = driver.find_element(By.ID, "attend-count")
    return to_int(el_streak.text), to_int(el_ruby.text), to_int(el_count.text)


driver, _ = setup()
wait = make_wait(driver, 10)

step("시작 상태 읽기")
driver.get(GAME_URL + "/attendance")
wait.until(EC.element_to_be_clickable((By.ID, "attend-btn")),
           message="출석하기 버튼이 준비되지 않음")

start_streak, start_ruby, start_count = read_status(driver)
print(f"연속 출석 {start_streak}일 · 루비 {start_ruby} · 요청 횟수 {start_count}")

step("연속 출석 7일을 채울 때까지 출석하기")
tries = 0
streak = start_streak
ok_tries = []
fail_tries = []
fail_msgs = []
shots = []
stop_reason = ""

while streak < TARGET_STREAK and tries < MAX_TRIES:
    tries = tries + 1
    el_attend_btn = driver.find_element(By.ID, "attend-btn")
    el_attend_btn.click()

    wait.until(lambda d: d.find_element(By.ID, "attend-msg").text != "",
               message=f"시도 {tries} 의 출석 결과가 나오지 않음")

    el_attend_msg = driver.find_element(By.ID, "attend-msg")
    msg = el_attend_msg.text

    if msg.startswith(SUCCESS_PREFIX):
        wait.until(lambda d: d.find_element(By.ID, "reward-state").text == REWARD_DONE,
                   message=f"시도 {tries} 의 보상 상태가 완료로 바뀌지 않음")
        ok_tries.append(tries)
        print(f" 시도 {tries}: {msg}")
    else:
        path = save_screenshot(driver, f"08_시도{tries}_실패")
        fail_tries.append(tries)
        fail_msgs.append(msg)
        shots.append(path)
        print(f" 시도 {tries}: {msg} · 증거 {os.path.basename(path)}")

    streak, ruby, count = read_status(driver)

    if len(fail_tries) > MAX_FAIL_ALLOWED:
        stop_reason = (f"한 번의 출석에서 실패가 너무 많습니다: "
                       f"기대 {MAX_FAIL_ALLOWED}회 이하, 실제 {len(fail_tries)}회 {fail_tries}")
        break

step("끝난 뒤 상태 확인")
end_streak, end_ruby, end_count = read_status(driver)
el_day7 = driver.find_element(By.ID, "day7")
day7_class = el_day7.get_attribute("class")
shot_done = save_screenshot(driver, "08_연속_7일_완료")

shot_names = [os.path.basename(path) for path in shots]
print(f"모두 {tries}번 시도해서 연속 출석 {end_streak}일을 채웠습니다")
print(f"실패한 시도 번호: {fail_tries} · 성공한 시도 {len(ok_tries)}회")
print(f"실패 문구: {fail_msgs}")
print(f"실패 증거 스크린샷: {shot_names}")
print(f"연속 출석 {end_streak} · 루비 {end_ruby} · 요청 횟수 {end_count} · 7일차 종류 {day7_class!r}")

driver.quit()


assert stop_reason == "", stop_reason

assert tries < MAX_TRIES, \
    f"시도 횟수가 한계에 닿았습니다: 기대 {MAX_TRIES}번 미만, 실제 {tries}번 · 실패 {fail_tries}"

assert (start_streak, start_ruby, start_count) == (0, 0, 0), \
    f"시작 상태: 기대 연속 0일·루비 0·요청 0, 실제 연속 {start_streak}일·루비 {start_ruby}·요청 {start_count}"

wrong_msgs = [msg for msg in fail_msgs if msg != FAIL_MSG]
assert len(wrong_msgs) == 0, f"실패 문구: 기대 {FAIL_MSG!r}, 실제 {wrong_msgs}"

assert fail_tries == EXPECTED_FAIL_TRIES, \
    f"실패한 시도 번호: 기대 {EXPECTED_FAIL_TRIES}, 실제 {fail_tries}"

assert len(shots) == len(EXPECTED_FAIL_TRIES), \
    f"실패 증거 스크린샷: 기대 {len(EXPECTED_FAIL_TRIES)}장, 실제 {len(shots)}장 {shot_names}"

missing_shots = [path for path in shots + [shot_done] if not os.path.exists(path)]
assert len(missing_shots) == 0, f"스크린샷 파일이 없습니다: {missing_shots}"

expected_ruby = start_ruby + len(ok_tries) * RUBY_REWARD
assert (end_streak, end_ruby) == (TARGET_STREAK, expected_ruby), \
    (f"보상: 기대 연속 {TARGET_STREAK}일·루비 {expected_ruby}, "
     f"실제 연속 {end_streak}일·루비 {end_ruby}")

assert tries == EXPECTED_TRIES, \
    f"연속 출석 7일을 채우는 데 든 시도: 기대 {EXPECTED_TRIES}번, 실제 {tries}번"
assert end_count == EXPECTED_TRIES, \
    f"요청 횟수: 기대 {EXPECTED_TRIES}, 실제 {end_count}"

assert day7_class == DAY7_CLASS, f"7일차 칸 종류: 기대 {DAY7_CLASS!r}, 실제 {day7_class!r}"

print("게임 실습 8 정답 통과")
