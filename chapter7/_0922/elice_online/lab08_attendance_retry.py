"""실습 8. 출석 체크 실패 증거 남기기와 재시도 · 정답 코드와 해설

화면 /attendance        테스트 케이스 6개 (TC-8-01 ~ TC-8-06)

이 실습이 확인하는 것은 3가지입니다.
  ① 실패한 시도에서 멈추지 않고 증거를 남긴 뒤 이어서 재시도하는가
  ② 스크린샷 이름에 시도 번호를 넣어 앞 증거를 덮어쓰지 않는가
  ③ 실패한 요청도 요청 횟수를 올린다는 규칙으로 루비 기대값을 계산하는가

되풀이가 끝나지 않을 수 있으므로 MAX_TRIES 로 한계를 두고, 한계에 닿으면 값으로 보고합니다.
"""
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from game_login import setup, make_wait, save_screenshot, GAME_URL

# ── 기획 데이터 (화면에서 읽지 않고 기획서 값을 코드에 적습니다)
TARGET_STREAK = 7
MAX_TRIES = 20                      # 끝나지 않는 반복을 막는 안전장치입니다
RUBY_REWARD = 50                    # 기획 데이터 · 출석 체크
SUCCESS_PREFIX = "출석 완료"
FAIL_MSG = "일시적인 오류로 출석 처리에 실패했습니다 (E503)"
REWARD_DONE = "보상 수령 완료"
MAX_FAIL_ALLOWED = 5                # 한 번의 출석에서 5회를 넘겨 실패하면 정책을 어긴 것입니다
EXPECTED_TRIES = 8
EXPECTED_FAIL_TRIES = [5]
DAY7_CLASS = "day done"


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


def read_status(driver):
    """연속 출석 · 루비 · 요청 횟수를 한 번에 읽어 3가지 값으로 반환합니다 (TC-8-01)."""
    el_streak = driver.find_element(By.ID, "streak")
    el_ruby = driver.find_element(By.ID, "ruby")
    el_count = driver.find_element(By.ID, "attend-count")
    return to_int(el_streak.text), to_int(el_ruby.text), to_int(el_count.text)


# =====================================================================
# 진행
# =====================================================================
driver, _ = setup()
wait = make_wait(driver, 10)

# ── TC-8-01. 시작 상태
step("시작 상태 읽기")
driver.get(GAME_URL + "/attendance")
# 화면이 준비되기 전에 값을 읽으면 아직 표시되지 않은 칸을 0으로 확인합니다
wait.until(EC.element_to_be_clickable((By.ID, "attend-btn")),
           message="출석하기 버튼이 준비되지 않음")

start_streak, start_ruby, start_count = read_status(driver)
print(f"연속 출석 {start_streak}일 · 루비 {start_ruby} · 요청 횟수 {start_count}")

# ── TC-8-02 · TC-8-03 · TC-8-04 · TC-8-05. 7일을 채울 때까지 되풀이
step("연속 출석 7일을 채울 때까지 출석하기")
tries = 0                  # 성공·실패를 가리지 않은 전체 시도 횟수입니다
streak = start_streak
ok_tries = []              # 성공한 시도 번호입니다 (루비 기대값을 이 개수로 계산합니다)
fail_tries = []            # 실패한 시도 번호입니다
fail_msgs = []             # 실패 문구를 그대로 모아 두어 기획서 문구와 비교합니다
shots = []                 # 실패 증거 스크린샷 경로입니다
stop_reason = ""           # 정책을 어겨 멈춘 이유입니다 (빈 글자가 정상입니다)

while streak < TARGET_STREAK and tries < MAX_TRIES:
    tries = tries + 1
    el_attend_btn = driver.find_element(By.ID, "attend-btn")
    el_attend_btn.click()

    # 누르는 순간 결과 칸이 먼저 비워집니다.
    # 기다리지 않고 읽으면 빈 글자를 결과로 확인합니다.
    # wait.until 은 조건을 0.5초 간격으로 다시 실행해 참이 될 때까지 기다립니다.
    # 그래서 인자로 「값」 이 아니라 「호출할 함수」 를 전달해야 합니다.
    #   d.find_element(...).text != ""      ← 지금 시점에서 한 번 계산한 True/False 입니다
    #   lambda d: d.find_element(...).text != ""  ← 회차마다 다시 계산하는 함수입니다
    # lambda 는 이름 없는 함수라 def 로 따로 정의하지 않고 조건 1개를 그대로 작성할 수 있고,
    # 매개변수 d 에는 wait 를 만들 때 지정한 driver 가 회차마다 전달됩니다
    wait.until(lambda d: d.find_element(By.ID, "attend-msg").text != "",
               message=f"시도 {tries} 의 출석 결과가 나오지 않음")

    el_attend_msg = driver.find_element(By.ID, "attend-msg")
    msg = el_attend_msg.text

    if msg.startswith(SUCCESS_PREFIX):
        # 보상 상태가 「보상 지급 중」 일 때 다시 누르면 요청 횟수만 오릅니다.
        # 다시 누르지 않고 완료로 바뀔 때까지 기다립니다
        wait.until(lambda d: d.find_element(By.ID, "reward-state").text == REWARD_DONE,
                   message=f"시도 {tries} 의 보상 상태가 완료로 바뀌지 않음")
        ok_tries.append(tries)
        print(f" 시도 {tries}: {msg}")
    else:
        # 실패한 시도마다 시도 번호를 이름에 넣습니다.
        # 이름을 하나로 쓰면 앞 시도의 증거를 덮어써 몇 번째가 실패했는지 남지 않습니다
        path = save_screenshot(driver, f"08_시도{tries}_실패")
        fail_tries.append(tries)
        fail_msgs.append(msg)
        shots.append(path)
        print(f" 시도 {tries}: {msg} · 증거 {os.path.basename(path)}")

    # 성공·실패를 가린 뒤 연속 출석을 다시 읽습니다.
    # 실패한 시도는 이 값을 올리지 않으므로 되풀이 조건이 그대로 유지됩니다
    streak, ruby, count = read_status(driver)

    if len(fail_tries) > MAX_FAIL_ALLOWED:
        # assert 로 바로 멈추면 남은 화면과 스크린샷이 남지 않습니다.
        # 이유를 변수에 보관하고 되풀이만 멈춥니다
        stop_reason = (f"한 번의 출석에서 실패가 너무 많습니다: "
                       f"기대 {MAX_FAIL_ALLOWED}회 이하, 실제 {len(fail_tries)}회 {fail_tries}")
        break

# ── TC-8-06. 끝난 뒤 상태
step("끝난 뒤 상태 확인")
end_streak, end_ruby, end_count = read_status(driver)
el_day7 = driver.find_element(By.ID, "day7")
day7_class = el_day7.get_attribute("class")
shot_done = save_screenshot(driver, "08_연속_7일_완료")

# 파일 경로는 폴더까지 들어 있어 출력이 길어집니다.
# 파일 이름만 모은 목록을 따로 만들어 어느 시도의 증거인지 한눈에 보이게 합니다
shot_names = [os.path.basename(path) for path in shots]
print(f"모두 {tries}번 시도해서 연속 출석 {end_streak}일을 채웠습니다")
print(f"실패한 시도 번호: {fail_tries} · 성공한 시도 {len(ok_tries)}회")
print(f"실패 문구: {fail_msgs}")
print(f"실패 증거 스크린샷: {shot_names}")
print(f"연속 출석 {end_streak} · 루비 {end_ruby} · 요청 횟수 {end_count} · 7일차 종류 {day7_class!r}")

driver.quit()


# =====================================================================
# 검증 (브라우저를 닫은 뒤 모아 둔 값을 한꺼번에 비교합니다)
# =====================================================================
# 정책을 어겨 멈춘 것이 있으면 다른 비교보다 먼저 보고합니다
assert stop_reason == "", stop_reason

# 되풀이가 한계에 닿아 끝난 것인지 먼저 가려냅니다.
# 이 확인이 없으면 「7일을 못 채웠다」 를 값이 틀린 것으로 잘못 보고합니다
assert tries < MAX_TRIES, \
    f"시도 횟수가 한계에 닿았습니다: 기대 {MAX_TRIES}번 미만, 실제 {tries}번 · 실패 {fail_tries}"

# TC-8-01. 시작 상태는 데이터 초기화 직후 값입니다
assert (start_streak, start_ruby, start_count) == (0, 0, 0), \
    f"시작 상태: 기대 연속 0일·루비 0·요청 0, 실제 연속 {start_streak}일·루비 {start_ruby}·요청 {start_count}"

# TC-8-02 · TC-8-03. 실패 문구는 기획서 문구와 글자까지 같아야 합니다.
# 기획서 문구와 다른 것만 모아 개수로 판정하면 어느 문구가 달랐는지 메시지에 남습니다
wrong_msgs = [msg for msg in fail_msgs if msg != FAIL_MSG]
assert len(wrong_msgs) == 0, f"실패 문구: 기대 {FAIL_MSG!r}, 실제 {wrong_msgs}"

# TC-8-03. 실패는 5의 배수 요청에서만 일어납니다
assert fail_tries == EXPECTED_FAIL_TRIES, \
    f"실패한 시도 번호: 기대 {EXPECTED_FAIL_TRIES}, 실제 {fail_tries}"

# TC-8-04. 증거는 실패한 시도마다 1장이고, 파일이 실제로 생겨야 합니다
assert len(shots) == len(EXPECTED_FAIL_TRIES), \
    f"실패 증거 스크린샷: 기대 {len(EXPECTED_FAIL_TRIES)}장, 실제 {len(shots)}장 {shot_names}"

# 없는 파일만 모아 개수로 판정하면 어느 파일이 없는지 메시지에 남습니다.
# 참·거짓 1개로 확인하면 어느 시도의 증거가 빠졌는지 알 수 없습니다
missing_shots = [path for path in shots + [shot_done] if not os.path.exists(path)]
assert len(missing_shots) == 0, f"스크린샷 파일이 없습니다: {missing_shots}"

# TC-8-05 · TC-8-06. 실패한 요청도 요청 횟수를 올리므로,
# 루비 기대값은 전체 시도가 아니라 성공한 시도 횟수로 계산합니다
expected_ruby = start_ruby + len(ok_tries) * RUBY_REWARD
assert (end_streak, end_ruby) == (TARGET_STREAK, expected_ruby), \
    (f"보상: 기대 연속 {TARGET_STREAK}일·루비 {expected_ruby}, "
     f"실제 연속 {end_streak}일·루비 {end_ruby}")

# TC-8-06. 시도 횟수와 요청 횟수는 성공 7회에 실패 1회를 더한 값입니다
assert tries == EXPECTED_TRIES, \
    f"연속 출석 7일을 채우는 데 든 시도: 기대 {EXPECTED_TRIES}번, 실제 {tries}번"
assert end_count == EXPECTED_TRIES, \
    f"요청 횟수: 기대 {EXPECTED_TRIES}, 실제 {end_count}"

# TC-8-06. 7일차 칸은 글자가 아니라 class 로 완료를 표시합니다
assert day7_class == DAY7_CLASS, f"7일차 칸 종류: 기대 {DAY7_CLASS!r}, 실제 {day7_class!r}"

print("게임 실습 8 정답 통과")
