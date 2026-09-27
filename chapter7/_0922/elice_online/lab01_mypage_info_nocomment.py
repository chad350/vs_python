from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from game_login import setup, save_screenshot, GAME_URL

SPEC_START = {"level": 10, "gold": 1000, "score": 0}
NEW_NICK = "탐험가"
CHECK_OK = "사용할 수 있는 닉네임입니다"
RESET_DONE = "데이터 초기화 완료"


def to_int(text):
    return int(text.replace(",", "").strip())


def read_my_page(driver, wait):
    driver.get(GAME_URL + "/me")
    wait.until(EC.presence_of_element_located((By.ID, "me-username")),
               message="마이페이지가 열리지 않음")

    el_username = driver.find_element(By.ID, "me-username")
    el_nickname = driver.find_element(By.ID, "me-nickname")
    el_level = driver.find_element(By.ID, "me-level")
    el_gold = driver.find_element(By.ID, "me-gold")
    el_score = driver.find_element(By.ID, "me-score")

    return {"username": el_username.text,
            "nickname": el_nickname.text,
            "level": el_level.text,
            "gold": el_gold.text,
            "score": el_score.text}


def read_header(driver, wait):
    wait.until(EC.presence_of_element_located((By.ID, "hdr-nick")),
               message="머리글이 보이지 않음")

    el_nick = driver.find_element(By.ID, "hdr-nick")
    el_gold = driver.find_element(By.ID, "hdr-gold")

    return {"nickname": el_nick.text, "gold": el_gold.text}


driver, wait = setup()

first_me = read_my_page(driver, wait)
print("처음 마이페이지:", first_me)

first_header = read_header(driver, wait)
print("처음 머리글:", first_header)

el_nick_new = driver.find_element(By.ID, "nick-new")
el_nick_new.clear()
el_nick_new.send_keys(NEW_NICK)

el_save_btn = driver.find_element(By.ID, "nick-save-btn")
save_enabled_before = el_save_btn.is_enabled()

el_check_btn = driver.find_element(By.ID, "nick-check-btn")
el_check_btn.click()

el_check_result = driver.find_element(By.ID, "nick-check-result")
check_right_after = el_check_result.text

wait.until(lambda d: d.find_element(By.ID, "nick-check-result").text != "",
           message="중복 검사 결과가 오지 않음")

check_after_wait = driver.find_element(By.ID, "nick-check-result").text
save_enabled_after = el_save_btn.is_enabled()
print(f"중복 검사 · 누른 직후 {check_right_after!r} → 1초 뒤 {check_after_wait!r}")
print(f"변경 버튼 · 검사 전 {save_enabled_before} → 검사 뒤 {save_enabled_after}")

el_save_btn.click()
wait.until(lambda d: d.find_element(By.ID, "me-nickname").text == NEW_NICK
           and d.find_element(By.ID, "hdr-nick").text == NEW_NICK,
           message="닉네임이 마이페이지와 머리글에 반영되지 않음")

changed_me = {"nickname": driver.find_element(By.ID, "me-nickname").text}
changed_header = {"nickname": driver.find_element(By.ID, "hdr-nick").text}
change_msg = driver.find_element(By.ID, "nick-msg").text

shot_changed = save_screenshot(driver, "01_닉네임_변경")

driver.get(GAME_URL + "/shop")
shop_header = read_header(driver, wait)
print(f"바꾼 뒤 · 마이페이지 {changed_me['nickname']} · 머리글 {changed_header['nickname']}"
      f" · 상점 머리글 {shop_header['nickname']} · 문구 {change_msg}")

driver.get(GAME_URL + "/me")
el_reset_btn = wait.until(EC.element_to_be_clickable((By.ID, "reset-btn")),
                          message="초기화 버튼을 누를 수 없음")
el_reset_btn.click()
wait.until(lambda d: d.find_element(By.ID, "reset-msg").text != "",
           message="초기화 결과 문구가 오지 않음")

reset_msg = driver.find_element(By.ID, "reset-msg").text
reset_me = read_my_page(driver, wait)
shot_reset = save_screenshot(driver, "01_초기화_뒤")
print(f"초기화 뒤 마이페이지: {reset_me} · 문구 {reset_msg}")

driver.quit()

assert int(first_me["level"]) == SPEC_START["level"], \
    f"레벨: 기대 {SPEC_START['level']}, 실제 {first_me['level']!r}"
assert int(first_me["score"]) == SPEC_START["score"], \
    f"점수: 기대 {SPEC_START['score']}, 실제 {first_me['score']!r}"

assert to_int(first_me["gold"]) == to_int(first_header["gold"]) == SPEC_START["gold"], \
    f"골드: 마이페이지 {first_me['gold']!r}, 머리글 {first_header['gold']!r}, 기획서 {SPEC_START['gold']}"
assert first_me["nickname"] == first_header["nickname"], \
    f"처음 닉네임: 마이페이지 {first_me['nickname']!r}, 머리글 {first_header['nickname']!r}"

assert save_enabled_before is False, f"검사 전 변경 버튼: 기대 비활성, 실제 {save_enabled_before}"
assert save_enabled_after is True, f"검사 뒤 변경 버튼: 기대 활성, 실제 {save_enabled_after}"

assert check_right_after == "", f"중복 검사 누른 직후: 기대 '', 실제 {check_right_after!r}"
assert check_after_wait == CHECK_OK, f"중복 검사 결과: 기대 {CHECK_OK!r}, 실제 {check_after_wait!r}"

assert changed_me["nickname"] == changed_header["nickname"] == shop_header["nickname"] == NEW_NICK, \
    f"바꾼 닉네임: 마이페이지 {changed_me['nickname']!r}, 머리글 {changed_header['nickname']!r}, 상점 머리글 {shop_header['nickname']!r}"
assert change_msg == f"닉네임 변경 완료: {NEW_NICK}", f"변경 문구: 실제 {change_msg!r}"

assert reset_msg == RESET_DONE, f"초기화 문구: 기대 {RESET_DONE!r}, 실제 {reset_msg!r}"
assert to_int(reset_me["gold"]) == SPEC_START["gold"], \
    f"초기화 뒤 골드: 기대 {SPEC_START['gold']}, 실제 {reset_me['gold']!r}"
assert int(reset_me["score"]) == SPEC_START["score"], \
    f"초기화 뒤 점수: 기대 {SPEC_START['score']}, 실제 {reset_me['score']!r}"
assert reset_me["nickname"] == NEW_NICK, \
    f"초기화 뒤 닉네임: 기대 {NEW_NICK!r} 유지, 실제 {reset_me['nickname']!r}"

import os
missing_shots = [p for p in (shot_changed, shot_reset) if not os.path.exists(p)]
assert len(missing_shots) == 0, f"스크린샷이 없습니다: {missing_shots}"

print("게임 실습 1 정답 통과")
