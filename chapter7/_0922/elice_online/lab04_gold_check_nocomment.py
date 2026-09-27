from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from game_login import setup, make_wait, close_dialog, save_screenshot, GAME_URL

START_GOLD = 1000
ITEM = {"item_id": 11, "name": "견습 단검", "price": 120}
EXPECTED_GOLD = START_GOLD - ITEM["price"]
EXPECTED_ROWS = 1


def to_int(text):
    return int(text.replace(",", "").replace("G", "").strip())


def open_shop(driver, wait):
    driver.get(GAME_URL + "/shop")
    wait.until(EC.presence_of_element_located((By.ID, f"buy-btn-{ITEM['item_id']}")),
               message="상점 표가 표시되지 않아 구매 버튼을 찾지 못함")


def read_shop_gold(driver):
    el_shop_gold = driver.find_element(By.ID, "shop-gold")
    el_header_gold = driver.find_element(By.ID, "hdr-gold")
    return to_int(el_shop_gold.text), to_int(el_header_gold.text)


driver, _ = setup()
wait = make_wait(driver, 10)

open_shop(driver, wait)
gold_before_shop, gold_before_header = read_shop_gold(driver)

el_buy_btn = driver.find_element(By.ID, f"buy-btn-{ITEM['item_id']}")
el_buy_btn.click()
wait.until(lambda d: d.find_element(By.ID, "shop-msg").text != "",
           message="구매 결과 문구가 나오지 않음")

el_shop_msg = driver.find_element(By.ID, "shop-msg")
buy_msg = el_shop_msg.text

dialog_title, dialog_message = close_dialog(driver, wait)

gold_after_shop, gold_after_header = read_shop_gold(driver)
shot_after_buy = save_screenshot(driver, "04_구매_직후_상점")

open_shop(driver, wait)
gold_after_reload, _ = read_shop_gold(driver)

driver.get(GAME_URL + "/me")
wait.until(EC.presence_of_element_located((By.ID, "me-gold")), message="마이페이지가 열리지 않음")
el_me_gold = driver.find_element(By.ID, "me-gold")
gold_me = to_int(el_me_gold.text)

driver.get(GAME_URL + "/inventory")
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


assert gold_before_shop == START_GOLD, f"구매 전 상점 골드: 기대 {START_GOLD}, 실제 {gold_before_shop}"
assert gold_before_header == START_GOLD, f"구매 전 머리글 골드: 기대 {START_GOLD}, 실제 {gold_before_header}"

assert buy_msg == f"구매 완료: {ITEM['name']} x1", \
    f"구매 결과 문구: 기대 '구매 완료: {ITEM['name']} x1', 실제 {buy_msg!r}"

assert dialog_title != "", f"Dialog 제목: 기대 값 있음, 실제 {dialog_title!r}"
assert dialog_message != "", f"Dialog 본문: 기대 값 있음, 실제 {dialog_message!r}"

assert gold_after_reload == EXPECTED_GOLD, \
    f"새로고침 뒤 상점 골드: 기대 {EXPECTED_GOLD}, 실제 {gold_after_reload}"
assert gold_me == EXPECTED_GOLD, f"마이페이지 골드: 기대 {EXPECTED_GOLD}, 실제 {gold_me}"

assert inventory_rows == EXPECTED_ROWS, \
    f"인벤토리 행 수: 기대 {EXPECTED_ROWS}, 실제 {inventory_rows}"

import os
missing_shots = [path for path in [shot_after_buy] if not os.path.exists(path)]
assert len(missing_shots) == 0, f"스크린샷이 없습니다: {missing_shots}"

assert gold_after_shop == EXPECTED_GOLD and gold_after_header == EXPECTED_GOLD, (
    f"구매 직후 보유 골드가 기획서와 다릅니다: 기대 {EXPECTED_GOLD}, "
    f"상점 {gold_after_shop}, 머리글 {gold_after_header}, "
    f"새로고침 뒤 상점 {gold_after_reload}, 마이페이지 {gold_me}")
