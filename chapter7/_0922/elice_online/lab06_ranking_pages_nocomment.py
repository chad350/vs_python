from selenium.webdriver.common.by import By

from game_login import setup, make_wait, save_screenshot, GAME_URL

SPEC_RANKING = []
for rank in range(1, 21):
    SPEC_RANKING.append({"rank": rank,
                         "nick": f"랭커{rank:02d}",
                         "score": 100000 - (rank - 1) * 3777})

ROWS_PER_PAGE = 10
TOTAL_TEXT = "전체 20명"
FIRST_SORT_TEXT = "내림차순"
ROW_SELECTOR = "#rank-table tbody tr"


def step(title):
    print(f"\n=== {title} ===")


def page_rows(driver):
    rows = []
    el_rows = driver.find_elements(By.CSS_SELECTOR, ROW_SELECTOR)

    for el_row in el_rows:
        el_rank = el_row.find_element(By.CSS_SELECTOR, "td.col-rank")
        el_nick = el_row.find_element(By.CSS_SELECTOR, "td.col-nick")
        el_score = el_row.find_element(By.CSS_SELECTOR, "td.col-score")

        rows.append({"rank": int(el_rank.text),
                     "nick": el_nick.text,
                     "score": int(el_score.text.replace(",", ""))})
    return rows


def page_number(driver):
    el_page = driver.find_element(By.ID, "rank-page")
    return el_page.text


def scores_of(rows):
    return [row["score"] for row in rows]


driver, _ = setup()
wait = make_wait(driver, 10)

step("1페이지 10행 수집")
driver.get(GAME_URL + "/ranking")
wait.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, ROW_SELECTOR)) == ROWS_PER_PAGE,
           message="랭킹 1페이지 10행이 표시되지 않음")

el_total = driver.find_element(By.ID, "rank-total")
total_text = el_total.text
el_sort_order = driver.find_element(By.ID, "rank-sort-order")
sort_text_first = el_sort_order.text

page1 = page_rows(driver)
print("1페이지:", [(row["rank"], row["score"]) for row in page1])

step("2페이지로 넘긴 뒤 10행 수집")
el_next_btn = driver.find_element(By.ID, "rank-next")
el_next_btn.click()
wait.until(lambda d: page_number(d) == "2", message="랭킹 2페이지가 표시되지 않음")

page2 = page_rows(driver)
el_rank_table = driver.find_element(By.ID, "rank-table")
shot_page2 = save_screenshot(driver, "06_랭킹_2페이지", el_rank_table)
print("2페이지:", [(row["rank"], row["score"]) for row in page2])

step("두 페이지 이어 붙여 기획서 표와 대조")
joined = page1 + page2
nicks = [row["nick"] for row in joined]

nick_counts = {}
for nick in nicks:
    nick_counts.setdefault(nick, 0)
    nick_counts[nick] = nick_counts[nick] + 1

duplicated = sorted([nick for nick in nick_counts if nick_counts[nick] > 1])
missing = [spec["nick"] for spec in SPEC_RANKING if spec["nick"] not in nicks]
print("이어붙인 행 수:", len(joined), "· 서로 다른 닉네임 수:", len(nick_counts))
print("겹쳐 나온 닉네임:", duplicated)
print("어느 페이지에도 없는 닉네임:", missing)

step("정렬 순서 확인")
page1_scores = scores_of(page1)
page2_scores = scores_of(page2)
page1_desc = page1_scores == sorted(page1_scores, reverse=True)
page2_desc = page2_scores == sorted(page2_scores, reverse=True)
pages_connected = page1_scores[-1] > page2_scores[0]
print(f"1페이지 내림차순 {page1_desc} · 2페이지 내림차순 {page2_desc} · 페이지 사이 이어짐 {pages_connected}")
print(f"1페이지 마지막 {page1_scores[-1]} · 2페이지 첫 {page2_scores[0]}")

step("점수 정렬 버튼 확인")
el_sort_btn = driver.find_element(By.ID, "rank-sort-score")
el_sort_btn.click()
wait.until(lambda d: d.find_element(By.ID, "rank-sort-order").text == "오름차순",
           message="정렬 문구가 오름차순으로 바뀌지 않음")
asc_scores = scores_of(page_rows(driver))

el_sort_btn.click()
wait.until(lambda d: d.find_element(By.ID, "rank-sort-order").text == "내림차순",
           message="정렬 문구가 내림차순으로 되돌아오지 않음")
restored_scores = scores_of(page_rows(driver))
print("오름차순으로 뒤집힌 점수:", asc_scores)
print("다시 내림차순:", restored_scores)

driver.quit()


assert total_text == TOTAL_TEXT, f"전체 인원 문구: 기대 {TOTAL_TEXT!r}, 실제 {total_text!r}"
assert sort_text_first == FIRST_SORT_TEXT, f"처음 정렬 문구: 기대 {FIRST_SORT_TEXT!r}, 실제 {sort_text_first!r}"

assert len(page1) == ROWS_PER_PAGE, f"1페이지 행 수: 기대 {ROWS_PER_PAGE}, 실제 {len(page1)}"
assert len(page2) == ROWS_PER_PAGE, f"2페이지 행 수: 기대 {ROWS_PER_PAGE}, 실제 {len(page2)}"
assert page1 == SPEC_RANKING[:ROWS_PER_PAGE], f"1페이지가 기획서 1~10위와 다릅니다: 실제 {page1}"

assert page1_desc and page2_desc, \
    f"페이지 안 내림차순: 1페이지 {page1_scores}, 2페이지 {page2_scores}"

assert asc_scores == sorted(asc_scores), f"정렬 버튼 뒤 오름차순: 실제 {asc_scores}"
assert restored_scores == page2_scores, \
    f"되돌린 뒤 차례: 기대 {page2_scores}, 실제 {restored_scores}"

import os
missing_shots = [path for path in [shot_page2] if not os.path.exists(path)]
assert len(missing_shots) == 0, f"스크린샷이 없습니다: {missing_shots}"

assert joined == SPEC_RANKING, (
    f"랭킹 두 페이지를 이어 붙인 목록이 기획서 20명과 다릅니다. "
    f"2페이지 첫 행: 기대 11위 랭커11 62230, 실제 {page2[0]['rank']}위 {page2[0]['nick']} {page2[0]['score']} "
    f"(1페이지 마지막 10위 {page1[-1]['score']}보다 점수가 큽니다). "
    f"겹쳐 나온 닉네임: 기대 [], 실제 {duplicated}. "
    f"어느 페이지에도 없는 닉네임: 기대 [], 실제 {missing}")
