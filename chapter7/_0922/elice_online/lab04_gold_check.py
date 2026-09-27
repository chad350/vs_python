"""실습 4. 구매 뒤 골드를 여러 화면에서 대조 · 정답 코드와 해설

화면 /shop · /me · /inventory        테스트 케이스 7개 (TC-4-01 ~ TC-4-07)

이 실습이 확인하는 것은 3가지입니다.
  ① 구매 결과 문구와 Dialog 를 기다린 뒤에 값을 읽는가
  ② 같은 골드를 상점 · 머리글 · 새로 연 상점 · 마이페이지 4개 화면에서 모아 기획서 기대값과 비교하는가
  ③ 기획서와 다른 값이 나왔을 때 기대값을 고치지 않고 4개 값을 한 메시지로 보고하는가

이 문항은 AssertionError 로 끝나는 것이 정답입니다 (종료 코드 1).
구매 직후 상점 화면의 골드가 기획서 기대값과 다르게 표시됩니다.
보고로 끝나는 assert 를 앞에 두면 나머지 값을 확인하지 못하므로, 4개 값을 모두 읽어 출력한 뒤 마지막에 보고합니다.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from game_login import setup, make_wait, close_dialog, save_screenshot, GAME_URL

# ── 기획 데이터 (화면에서 읽지 않고 기획서 값을 코드에 적습니다)
START_GOLD = 1000
ITEM = {"item_id": 11, "name": "견습 단검", "price": 120}
EXPECTED_GOLD = START_GOLD - ITEM["price"]              # 기획서 가격으로 계산한 880
EXPECTED_ROWS = 1                                       # 구매하면 인벤토리에 1행이 생깁니다


def to_int(text):
    """'1,000' 처럼 쉼표가 든 글자를 정수로 바꿉니다.

    화면에서 얻은 데이터는 문자열로 저장되고, 상점은 1,000 · 머리글은 1000 으로 표기가 다릅니다.
    쉼표와 단위를 지운 뒤 정수로 바꿔야 4개 화면의 값을 같은 기준으로 비교할 수 있습니다.
    """
    return int(text.replace(",", "").replace("G", "").strip())


def open_shop(driver, wait):
    """상점을 열고 구매 버튼이 나타날 때까지 기다립니다.

    표가 표시되기 전에는 구매 버튼이 없어 NoSuchElementException 이 발생합니다.
    """
    driver.get(GAME_URL + "/shop")
    wait.until(EC.presence_of_element_located((By.ID, f"buy-btn-{ITEM['item_id']}")),
               message="상점 표가 표시되지 않아 구매 버튼을 찾지 못함")


def read_shop_gold(driver):
    """상점 화면의 보유 골드와 머리글 골드를 정수 2개로 반환합니다."""
    el_shop_gold = driver.find_element(By.ID, "shop-gold")
    el_header_gold = driver.find_element(By.ID, "hdr-gold")
    return to_int(el_shop_gold.text), to_int(el_header_gold.text)


# =====================================================================
# 진행
# =====================================================================
driver, _ = setup()
wait = make_wait(driver, 10)

# ── TC-4-01. 구매 전 상점 골드와 머리글 골드
open_shop(driver, wait)
gold_before_shop, gold_before_header = read_shop_gold(driver)

# ── TC-4-02. 구매 버튼을 누르고 결과 문구 기다리기
# 누르는 순간 결과 칸이 먼저 비워집니다.
# 기다리지 않고 읽으면 구매가 끝났는지 알 수 없는 값을 읽습니다.
# wait.until 은 조건을 0.5초 간격으로 다시 실행해 참이 될 때까지 기다립니다.
# 그래서 인자로 「값」 이 아니라 「호출할 함수」 를 전달해야 합니다.
#   d.find_element(...).text != ""      ← 지금 시점에서 한 번 계산한 True/False 입니다
#   lambda d: d.find_element(...).text != ""  ← 회차마다 다시 계산하는 함수입니다
# lambda 는 이름 없는 함수라 def 로 따로 정의하지 않고 조건 1개를 그대로 작성할 수 있고,
# 매개변수 d 에는 wait 를 만들 때 지정한 driver 가 회차마다 전달됩니다
el_buy_btn = driver.find_element(By.ID, f"buy-btn-{ITEM['item_id']}")
el_buy_btn.click()
wait.until(lambda d: d.find_element(By.ID, "shop-msg").text != "",
           message="구매 결과 문구가 나오지 않음")

el_shop_msg = driver.find_element(By.ID, "shop-msg")
buy_msg = el_shop_msg.text

# ── TC-4-03. Dialog 닫기
# 이 Dialog 는 showModal() 로 열려 있어 바깥 요소를 누르면 ElementClickInterceptedException 이 납니다.
# 제공 코드의 close_dialog() 가 열림 확인 · 제목과 본문 읽기 · 닫힘 확인을 한 번에 처리합니다
dialog_title, dialog_message = close_dialog(driver, wait)

# ── TC-4-07. 구매 직후 같은 화면의 골드 (이 문항이 보고할 값)
gold_after_shop, gold_after_header = read_shop_gold(driver)
shot_after_buy = save_screenshot(driver, "04_구매_직후_상점")

# ── TC-4-04. 상점을 새로 열었을 때의 골드
open_shop(driver, wait)
gold_after_reload, _ = read_shop_gold(driver)

# ── TC-4-05. 마이페이지 골드
driver.get(GAME_URL + "/me")
wait.until(EC.presence_of_element_located((By.ID, "me-gold")), message="마이페이지가 열리지 않음")
el_me_gold = driver.find_element(By.ID, "me-gold")
gold_me = to_int(el_me_gold.text)

# ── TC-4-06. 인벤토리 행 개수
driver.get(GAME_URL + "/inventory")
# 행 개수를 회차마다 다시 세야 하므로 조건을 함수로 전달합니다
wait.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, "#inv-table tbody tr")) > 0,
           message="인벤토리 표가 표시되지 않음")
el_inv_rows = driver.find_elements(By.CSS_SELECTOR, "#inv-table tbody tr")
inventory_rows = len(el_inv_rows)

driver.quit()

print(f"구매 문구: {buy_msg!r} · Dialog {dialog_title!r}")
print(f"구매 전 골드 · 상점 {gold_before_shop} / 머리글 {gold_before_header} / 기대 {START_GOLD}")
print(f"구매 뒤 골드 · 상점 {gold_after_shop} / 머리글 {gold_after_header} / "
      f"새로고침 뒤 상점 {gold_after_reload} / 마이페이지 {gold_me} / 기대 {EXPECTED_GOLD}")
print(f"인벤토리 행 수 · 화면 {inventory_rows} / 기대 {EXPECTED_ROWS}")


# =====================================================================
# 검증 (브라우저를 닫은 뒤 모아 둔 값을 한꺼번에 비교합니다)
# =====================================================================
# TC-4-01. 구매 전에는 두 화면 모두 초기 골드입니다
assert gold_before_shop == START_GOLD, f"구매 전 상점 골드: 기대 {START_GOLD}, 실제 {gold_before_shop}"
assert gold_before_header == START_GOLD, f"구매 전 머리글 골드: 기대 {START_GOLD}, 실제 {gold_before_header}"

# TC-4-02. 구매 결과 문구
assert buy_msg == f"구매 완료: {ITEM['name']} x1", \
    f"구매 결과 문구: 기대 '구매 완료: {ITEM['name']} x1', 실제 {buy_msg!r}"

# TC-4-03. Dialog 제목과 본문을 읽었는지 (close_dialog 가 닫힘까지 확인합니다)
assert dialog_title != "", f"Dialog 제목: 기대 값 있음, 실제 {dialog_title!r}"
assert dialog_message != "", f"Dialog 본문: 기대 값 있음, 실제 {dialog_message!r}"

# TC-4-04 · TC-4-05. 새로 연 화면 2개는 기획서 기대값과 같습니다.
# 이 2가지가 통과해야 「구매는 처리되었다」 는 사실이 확인되고,
# 마지막 보고를 「화면 갱신 문제」 로 좁힐 수 있습니다
assert gold_after_reload == EXPECTED_GOLD, \
    f"새로고침 뒤 상점 골드: 기대 {EXPECTED_GOLD}, 실제 {gold_after_reload}"
assert gold_me == EXPECTED_GOLD, f"마이페이지 골드: 기대 {EXPECTED_GOLD}, 실제 {gold_me}"

# TC-4-06. 인벤토리 행 개수
assert inventory_rows == EXPECTED_ROWS, \
    f"인벤토리 행 수: 기대 {EXPECTED_ROWS}, 실제 {inventory_rows}"

# 스크린샷이 실제로 저장되었는지 확인합니다 (save_screenshot 이 파일 경로를 반환합니다)
import os
# 없는 파일만 컴프리헨션으로 모아 개수로 판정합니다.
# 참·거짓 1개로 확인하면 어느 파일이 없는지 메시지에 남지 않습니다
missing_shots = [path for path in [shot_after_buy] if not os.path.exists(path)]
assert len(missing_shots) == 0, f"스크린샷이 없습니다: {missing_shots}"

# TC-4-07. 기획서와 다른 값이 나와도 기대값을 화면 값으로 바꾸지 않습니다.
# 4개 값을 한 메시지에 적어 두면, 보고를 받는 사람이 구매 처리와 화면 갱신 중 어느 것이 문제인지 가릴 수 있습니다
assert gold_after_shop == EXPECTED_GOLD and gold_after_header == EXPECTED_GOLD, (
    f"구매 직후 보유 골드가 기획서와 다릅니다: 기대 {EXPECTED_GOLD}, "
    f"상점 {gold_after_shop}, 머리글 {gold_after_header}, "
    f"새로고침 뒤 상점 {gold_after_reload}, 마이페이지 {gold_me}")
