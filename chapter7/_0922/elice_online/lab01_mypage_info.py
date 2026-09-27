"""실습 1. 마이페이지 정보 추출과 닉네임 변경 · 정답 코드와 해설

화면 /me · 머리글 · /shop        테스트 케이스 8개 (TC-1-01 ~ TC-1-08)

이 실습이 확인하는 것은 3가지입니다.
  ① 마이페이지가 보여 주는 계정 값 5가지가 머리글 값과 기획서 초기값과 맞는가
  ② 닉네임 중복 검사 결과가 1초 뒤에 오는 것을 코드가 기다리는가
  ③ 바꾼 닉네임이 마이페이지 · 머리글 · 새로 연 화면 세 곳에 모두 반영되고 저장까지 되는가

읽은 값은 읽는 즉시 판단하지 않고 변수에 모아 두고, 브라우저를 닫은 뒤 마지막에 한꺼번에 비교합니다.
중간에 assert 로 멈추면 남은 화면을 확인하지 못하고 스크린샷도 남지 않기 때문입니다.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from game_login import setup, save_screenshot, GAME_URL

# ── 기획 데이터 (화면에서 읽지 않고 기획서 값을 코드에 적습니다)
# 화면이 이 값과 다르면 기대값을 고치지 않고 「다르다」 고 보고합니다.
SPEC_START = {"level": 10, "gold": 1000, "score": 0}
NEW_NICK = "탐험가"                                     # 2~8자 규칙을 지키는 새 닉네임
CHECK_OK = "사용할 수 있는 닉네임입니다"                  # 중복 검사 통과 문구
RESET_DONE = "데이터 초기화 완료"                        # 초기화 완료 문구


def to_int(text):
    """'1,000' 처럼 쉼표가 든 글자를 정수로 바꿉니다.

    화면에서 읽은 데이터는 모두 문자열이라 '10' == 10 이 False 가 됩니다.
    그대로 int() 에 넣으면 쉼표 때문에 ValueError 가 나므로, 쉼표를 지우고 양쪽 공백을 없앤 뒤 바꿉니다.
    """
    return int(text.replace(",", "").strip())


def read_my_page(driver, wait):
    """마이페이지의 계정 값 5가지를 딕셔너리 하나로 모읍니다 (TC-1-01)."""
    driver.get(GAME_URL + "/me")
    # 화면이 뜨기 전에 찾으면 NoSuchElementException 이 나므로, 첫 요소가 나타날 때까지 기다립니다
    wait.until(EC.presence_of_element_located((By.ID, "me-username")),
               message="마이페이지가 열리지 않음")

    # 요소를 변수에 저장한 뒤 .text 를 읽습니다.
    # 어떤 요소를 읽는지 변수 이름으로 남습니다
    el_username = driver.find_element(By.ID, "me-username")
    el_nickname = driver.find_element(By.ID, "me-nickname")
    el_level = driver.find_element(By.ID, "me-level")
    el_gold = driver.find_element(By.ID, "me-gold")
    el_score = driver.find_element(By.ID, "me-score")

    # 값 5가지를 따로 변수로 두지 않고 딕셔너리 하나로 모읍니다.
    # 이렇게 하면 처음 값 · 바꾼 뒤 값 · 초기화 뒤 값을 같은 모양으로 비교할 수 있습니다
    return {"username": el_username.text,
            "nickname": el_nickname.text,
            "level": el_level.text,
            "gold": el_gold.text,
            "score": el_score.text}


def read_header(driver, wait):
    """머리글의 닉네임과 골드를 딕셔너리로 모읍니다 (TC-1-02)."""
    wait.until(EC.presence_of_element_located((By.ID, "hdr-nick")),
               message="머리글이 보이지 않음")

    el_nick = driver.find_element(By.ID, "hdr-nick")
    el_gold = driver.find_element(By.ID, "hdr-gold")

    # 머리글 골드는 1000, 마이페이지 골드는 1,000 으로 표기만 다릅니다.
    # 여기서는 화면 글자를 그대로 보관하고, 비교할 때 to_int 로 바꿥니다
    return {"nickname": el_nick.text, "gold": el_gold.text}


# =====================================================================
# 진행
# =====================================================================
# 제공 코드가 로그인 · 데이터 초기화 · 닉네임 되돌리기까지 끝내 줍니다.
# 그래서 이 코드는 매번 같은 상태(골드 1,000 · 점수 0 · 닉네임 수련생)에서 시작합니다.
driver, wait = setup()

# ── TC-1-01. 마이페이지 값 5가지
first_me = read_my_page(driver, wait)
print("처음 마이페이지:", first_me)

# ── TC-1-02. 머리글 값 2가지
# 머리글은 모든 화면에 있으므로 화면을 다시 열지 않고 지금 화면에서 읽습니다
first_header = read_header(driver, wait)
print("처음 머리글:", first_header)

# ── TC-1-03. 새 닉네임을 입력한 직후의 변경 버튼 상태
el_nick_new = driver.find_element(By.ID, "nick-new")
el_nick_new.clear()                                     # 앞 실행의 글자가 남아 있을 수 있습니다
el_nick_new.send_keys(NEW_NICK)

el_save_btn = driver.find_element(By.ID, "nick-save-btn")
# 중복 검사를 통과해야 켜지는 버튼입니다.
# 지금은 비활성이어야 정상입니다.
# 활성 여부는 글자가 아니라 is_enabled() 로 판단합니다
save_enabled_before = el_save_btn.is_enabled()

# ── TC-1-04. 중복 검사 버튼을 누른 직후의 결과 칸
el_check_btn = driver.find_element(By.ID, "nick-check-btn")
el_check_btn.click()

el_check_result = driver.find_element(By.ID, "nick-check-result")
# 결과는 1초 뒤에 옵니다.
# 기다리지 않고 읽으면 빈 글자를 읽습니다.
# 이 빈 글자를 「결과」 로 착각하는 것이 이 실습에서 확인하려는 실수입니다
check_right_after = el_check_result.text

# ── TC-1-05. 결과가 채워질 때까지 기다린 뒤 다시 읽기
# 「비어 있지 않을 때까지」 를 조건으로 씁니다.
# 특정 문구를 조건으로 두면
# 다른 문구가 왔을 때 TimeoutException 이 나서 실제 문구를 보고할 수 없습니다
# wait.until 은 조건을 0.5초 간격으로 다시 실행해 참이 될 때까지 기다립니다.
# 그래서 인자로 「값」 이 아니라 「호출할 함수」 를 전달해야 합니다.
#   d.find_element(...).text != ""      ← 지금 시점에서 한 번 계산한 True/False 입니다
#   lambda d: d.find_element(...).text != ""  ← 회차마다 다시 계산하는 함수입니다
# lambda 는 이름 없는 함수라 def 로 따로 정의하지 않고 조건 1개를 그대로 작성할 수 있고,
# 매개변수 d 에는 wait 를 만들 때 지정한 driver 가 회차마다 전달됩니다
wait.until(lambda d: d.find_element(By.ID, "nick-check-result").text != "",
           message="중복 검사 결과가 오지 않음")

check_after_wait = driver.find_element(By.ID, "nick-check-result").text
# 버튼 상태는 검사 결과가 온 뒤에 다시 읽습니다.
# 앞에서 저장한 el_save_btn 을 그대로 씁니다
save_enabled_after = el_save_btn.is_enabled()
print(f"중복 검사 · 누른 직후 {check_right_after!r} → 1초 뒤 {check_after_wait!r}")
print(f"변경 버튼 · 검사 전 {save_enabled_before} → 검사 뒤 {save_enabled_after}")

# ── TC-1-06. 변경 버튼을 누르고 두 곳이 바뀔 때까지 기다리기
el_save_btn.click()
# 마이페이지와 머리글이 각각 다른 시점에 바뀔 수 있으므로, 두 조건을 and 로 이어 함께 기다립니다.
# 하나만 기다리면 아직 바뀌지 않은 쪽을 읽어 비교가 어긋납니다
# 조건이 2가지여도 wait.until 에 전달하는 것은 lambda 로 만든 함수 1개입니다
wait.until(lambda d: d.find_element(By.ID, "me-nickname").text == NEW_NICK
           and d.find_element(By.ID, "hdr-nick").text == NEW_NICK,
           message="닉네임이 마이페이지와 머리글에 반영되지 않음")

changed_me = {"nickname": driver.find_element(By.ID, "me-nickname").text}
changed_header = {"nickname": driver.find_element(By.ID, "hdr-nick").text}
change_msg = driver.find_element(By.ID, "nick-msg").text

# 값을 모두 읽은 뒤에 찍습니다.
# 먼저 찍으면 아직 바뀌지 않은 화면이 남습니다
shot_changed = save_screenshot(driver, "01_닉네임_변경")

# ── TC-1-07. 새로 연 화면에서도 같은 닉네임인지 (저장 확인)
# 화면을 새로 열면 서버에서 값을 다시 받아옵니다.
# 그래도 바뀐 값이 나오면 화면에만 바뀐 것이 아니라 저장된 것입니다
driver.get(GAME_URL + "/shop")
shop_header = read_header(driver, wait)
print(f"바꾼 뒤 · 마이페이지 {changed_me['nickname']} · 머리글 {changed_header['nickname']}"
      f" · 상점 머리글 {shop_header['nickname']} · 문구 {change_msg}")

# ── TC-1-08. 데이터 초기화가 무엇을 되돌리고 무엇을 그대로 두는가
driver.get(GAME_URL + "/me")
el_reset_btn = wait.until(EC.element_to_be_clickable((By.ID, "reset-btn")),
                          message="초기화 버튼을 누를 수 없음")
el_reset_btn.click()
# 결과 문구가 나오기 전에 화면을 다시 열면 초기화 전의 값을 읽습니다
# 초기화 결과 문구도 회차마다 다시 읽어야 하므로 lambda 로 조건을 전달합니다
wait.until(lambda d: d.find_element(By.ID, "reset-msg").text != "",
           message="초기화 결과 문구가 오지 않음")

reset_msg = driver.find_element(By.ID, "reset-msg").text
# 초기화 뒤의 값은 화면을 다시 열어서 읽습니다 (서버에 저장된 값을 확인하기 위해서입니다)
reset_me = read_my_page(driver, wait)
shot_reset = save_screenshot(driver, "01_초기화_뒤")
print(f"초기화 뒤 마이페이지: {reset_me} · 문구 {reset_msg}")

driver.quit()

# =====================================================================
# 검증 (브라우저를 닫은 뒤 모아 둔 값을 한꺼번에 비교합니다)
# =====================================================================
# TC-1-01. 레벨 · 점수는 문자열이라 정수로 바꾼 뒤 기획서 값과 비교합니다
assert int(first_me["level"]) == SPEC_START["level"], \
    f"레벨: 기대 {SPEC_START['level']}, 실제 {first_me['level']!r}"
assert int(first_me["score"]) == SPEC_START["score"], \
    f"점수: 기대 {SPEC_START['score']}, 실제 {first_me['score']!r}"

# TC-1-02. 골드는 표기가 다르므로 쉼표를 지우고 정수로 바꿔 세 값을 한 번에 비교합니다
assert to_int(first_me["gold"]) == to_int(first_header["gold"]) == SPEC_START["gold"], \
    f"골드: 마이페이지 {first_me['gold']!r}, 머리글 {first_header['gold']!r}, 기획서 {SPEC_START['gold']}"
assert first_me["nickname"] == first_header["nickname"], \
    f"처음 닉네임: 마이페이지 {first_me['nickname']!r}, 머리글 {first_header['nickname']!r}"

# TC-1-03 · TC-1-05. 변경 버튼은 검사 전 비활성, 검사 뒤 활성입니다
assert save_enabled_before is False, f"검사 전 변경 버튼: 기대 비활성, 실제 {save_enabled_before}"
assert save_enabled_after is True, f"검사 뒤 변경 버튼: 기대 활성, 실제 {save_enabled_after}"

# TC-1-04. 누른 직후에는 결과가 아직 없어야 합니다
assert check_right_after == "", f"중복 검사 누른 직후: 기대 '', 실제 {check_right_after!r}"
assert check_after_wait == CHECK_OK, f"중복 검사 결과: 기대 {CHECK_OK!r}, 실제 {check_after_wait!r}"

# TC-1-06 · TC-1-07. 세 화면의 닉네임을 한 번에 비교합니다.
# 한 곳만 보면 머리글만 바뀌지 않는 결함을 놓칩니다
assert changed_me["nickname"] == changed_header["nickname"] == shop_header["nickname"] == NEW_NICK, \
    f"바꾼 닉네임: 마이페이지 {changed_me['nickname']!r}, 머리글 {changed_header['nickname']!r}, 상점 머리글 {shop_header['nickname']!r}"
assert change_msg == f"닉네임 변경 완료: {NEW_NICK}", f"변경 문구: 실제 {change_msg!r}"

# TC-1-08. 초기화는 골드 · 점수를 되돌리고 닉네임은 그대로 둡니다
assert reset_msg == RESET_DONE, f"초기화 문구: 기대 {RESET_DONE!r}, 실제 {reset_msg!r}"
assert to_int(reset_me["gold"]) == SPEC_START["gold"], \
    f"초기화 뒤 골드: 기대 {SPEC_START['gold']}, 실제 {reset_me['gold']!r}"
assert int(reset_me["score"]) == SPEC_START["score"], \
    f"초기화 뒤 점수: 기대 {SPEC_START['score']}, 실제 {reset_me['score']!r}"
assert reset_me["nickname"] == NEW_NICK, \
    f"초기화 뒤 닉네임: 기대 {NEW_NICK!r} 유지, 실제 {reset_me['nickname']!r}"

# 스크린샷 2개가 실제로 저장되었는지도 확인합니다 (save_screenshot 이 경로를 반환합니다)
import os
# 없는 파일만 컴프리헨션으로 모아 개수로 판정합니다.
# 참·거짓 1개로 확인하면 어느 파일이 없는지 실패 메시지에 남지 않습니다
missing_shots = [p for p in (shot_changed, shot_reset) if not os.path.exists(p)]
assert len(missing_shots) == 0, f"스크린샷이 없습니다: {missing_shots}"

print("게임 실습 1 정답 통과")
