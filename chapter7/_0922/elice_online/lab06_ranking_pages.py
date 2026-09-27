"""실습 6. 랭킹 정렬·페이지 넘김 검증 · 정답 코드와 해설

화면 /ranking        테스트 케이스 6개 (TC-6-01 ~ TC-6-06)

이 실습이 확인하는 것은 3가지입니다.
  ① 페이지를 바꾼 뒤 페이지 번호를 신호로 삼아 새 행을 읽는가
  ② 정렬을 첫 행 하나가 아니라 페이지 안 차례와 페이지 사이 이어짐으로 확인하는가
  ③ 두 페이지를 이어 붙인 20행이 기획서 20명과 한 번씩 같은지 확인하는가

이 문항은 AssertionError 로 끝나는 것이 정답입니다 (종료 코드 1).
2페이지가 기획서와 다르게 표시되며, 겹친 닉네임과 빠진 닉네임을 세어 한 메시지로 보고합니다.
"""
from selenium.webdriver.common.by import By

from game_login import setup, make_wait, save_screenshot, GAME_URL

# ── 기획 데이터 (화면에서 읽지 않고 기획서 값을 코드에 적습니다)
# 기획서의 점수 식은 100000 - (순위 - 1) x 3777 입니다.
# 식으로 20명을 만들어 두면 화면 값이 달라져도 기대값이 흔들리지 않습니다.
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
    """진행 단계를 출력합니다.

    어느 단계의 값인지 출력에서 구분하기 위해서입니다.
    """
    print(f"\n=== {title} ===")


def page_rows(driver):
    """지금 표시된 10행을 순위 · 닉네임 · 점수 딕셔너리 목록으로 모읍니다 (TC-6-02)."""
    rows = []
    el_rows = driver.find_elements(By.CSS_SELECTOR, ROW_SELECTOR)

    for el_row in el_rows:
        el_rank = el_row.find_element(By.CSS_SELECTOR, "td.col-rank")
        el_nick = el_row.find_element(By.CSS_SELECTOR, "td.col-nick")
        el_score = el_row.find_element(By.CSS_SELECTOR, "td.col-score")

        # 화면 점수는 100,000 처럼 쉼표가 들어 있어 그대로 int() 에 넣으면 ValueError 가 발생합니다
        rows.append({"rank": int(el_rank.text),
                     "nick": el_nick.text,
                     "score": int(el_score.text.replace(",", ""))})
    return rows


def page_number(driver):
    """현재 페이지 번호 글자를 반환합니다.

    새 페이지가 표시된 신호로 사용합니다.
    """
    el_page = driver.find_element(By.ID, "rank-page")
    return el_page.text


def scores_of(rows):
    """행 목록에서 점수만 뽑은 목록을 만듭니다."""
    return [row["score"] for row in rows]


# =====================================================================
# 진행
# =====================================================================
driver, _ = setup()
wait = make_wait(driver, 10)

# ── TC-6-01. 전체 인원 문구와 처음 정렬 문구
step("1페이지 10행 수집")
driver.get(GAME_URL + "/ranking")
# wait.until 은 조건을 0.5초 간격으로 다시 실행해 참이 될 때까지 기다립니다.
# 그래서 인자로 「값」 이 아니라 「호출할 함수」 를 전달해야 합니다.
#   len(driver.find_elements(...)) == 10      ← 지금 시점에서 한 번 계산한 True/False 입니다
#   lambda d: len(d.find_elements(...)) == 10 ← 회차마다 다시 세는 함수입니다
# lambda 는 이름 없는 함수라 def 로 따로 정의하지 않고 조건 1개를 그대로 작성할 수 있고,
# 매개변수 d 에는 wait 를 만들 때 지정한 driver 가 회차마다 전달됩니다
wait.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, ROW_SELECTOR)) == ROWS_PER_PAGE,
           message="랭킹 1페이지 10행이 표시되지 않음")

el_total = driver.find_element(By.ID, "rank-total")
total_text = el_total.text
el_sort_order = driver.find_element(By.ID, "rank-sort-order")
sort_text_first = el_sort_order.text

# ── TC-6-02. 1페이지 10행
page1 = page_rows(driver)
print("1페이지:", [(row["rank"], row["score"]) for row in page1])

# ── TC-6-03. 다음 페이지로 넘긴 뒤 10행
step("2페이지로 넘긴 뒤 10행 수집")
el_next_btn = driver.find_element(By.ID, "rank-next")
el_next_btn.click()
# 페이지 번호는 표를 다시 만든 뒤에 바뀝니다.
# 번호가 바뀌기 전에 읽으면 1페이지 행을 2페이지 값으로 모읍니다
wait.until(lambda d: page_number(d) == "2", message="랭킹 2페이지가 표시되지 않음")

page2 = page_rows(driver)
el_rank_table = driver.find_element(By.ID, "rank-table")
shot_page2 = save_screenshot(driver, "06_랭킹_2페이지", el_rank_table)
print("2페이지:", [(row["rank"], row["score"]) for row in page2])

# ── TC-6-06. 두 페이지를 이어 붙여 기획서 표와 대조
step("두 페이지 이어 붙여 기획서 표와 대조")
joined = page1 + page2
nicks = [row["nick"] for row in joined]

# 닉네임마다 몇 번 나왔는지 세어 두면, 겹친 닉네임을 목록으로 보고할 수 있습니다
nick_counts = {}
for nick in nicks:
    nick_counts.setdefault(nick, 0)
    nick_counts[nick] = nick_counts[nick] + 1

duplicated = sorted([nick for nick in nick_counts if nick_counts[nick] > 1])
missing = [spec["nick"] for spec in SPEC_RANKING if spec["nick"] not in nicks]
print("이어붙인 행 수:", len(joined), "· 서로 다른 닉네임 수:", len(nick_counts))
print("겹쳐 나온 닉네임:", duplicated)
print("어느 페이지에도 없는 닉네임:", missing)

# ── TC-6-04. 페이지 안 차례와 페이지 사이 이어짐
step("정렬 순서 확인")
page1_scores = scores_of(page1)
page2_scores = scores_of(page2)
page1_desc = page1_scores == sorted(page1_scores, reverse=True)
page2_desc = page2_scores == sorted(page2_scores, reverse=True)
# 페이지 안이 내림차순이어도 1페이지 마지막보다 2페이지 첫 점수가 크면 전체 차례는 어긋납니다.
# 첫 행 하나만 보면 이 어긋남을 확인하지 못합니다
pages_connected = page1_scores[-1] > page2_scores[0]
print(f"1페이지 내림차순 {page1_desc} · 2페이지 내림차순 {page2_desc} · 페이지 사이 이어짐 {pages_connected}")
print(f"1페이지 마지막 {page1_scores[-1]} · 2페이지 첫 {page2_scores[0]}")

# ── TC-6-05. 점수 정렬 버튼
step("점수 정렬 버튼 확인")
el_sort_btn = driver.find_element(By.ID, "rank-sort-score")
el_sort_btn.click()
# 정렬 문구가 바뀌는 것을 신호로 삼습니다.
# 누른 직후에 읽으면 뒤집히기 전 차례를 모읍니다
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


# =====================================================================
# 검증 (브라우저를 닫은 뒤 모아 둔 값을 한꺼번에 비교합니다)
# =====================================================================
# TC-6-01. 전체 인원 문구와 처음 정렬 문구
assert total_text == TOTAL_TEXT, f"전체 인원 문구: 기대 {TOTAL_TEXT!r}, 실제 {total_text!r}"
assert sort_text_first == FIRST_SORT_TEXT, f"처음 정렬 문구: 기대 {FIRST_SORT_TEXT!r}, 실제 {sort_text_first!r}"

# TC-6-02 · TC-6-03. 두 페이지 모두 10행이고, 1페이지는 기획서 1~10위와 같습니다
assert len(page1) == ROWS_PER_PAGE, f"1페이지 행 수: 기대 {ROWS_PER_PAGE}, 실제 {len(page1)}"
assert len(page2) == ROWS_PER_PAGE, f"2페이지 행 수: 기대 {ROWS_PER_PAGE}, 실제 {len(page2)}"
assert page1 == SPEC_RANKING[:ROWS_PER_PAGE], f"1페이지가 기획서 1~10위와 다릅니다: 실제 {page1}"

# TC-6-04. 페이지 안은 각각 내림차순입니다
assert page1_desc and page2_desc, \
    f"페이지 안 내림차순: 1페이지 {page1_scores}, 2페이지 {page2_scores}"

# TC-6-05. 정렬 버튼을 누르면 뒤집히고, 한 번 더 누르면 앞 차례로 되돌아옵니다
assert asc_scores == sorted(asc_scores), f"정렬 버튼 뒤 오름차순: 실제 {asc_scores}"
assert restored_scores == page2_scores, \
    f"되돌린 뒤 차례: 기대 {page2_scores}, 실제 {restored_scores}"

# 없는 파일만 모아 개수로 판정하면 어느 스크린샷이 없는지 메시지에 남습니다
import os
missing_shots = [path for path in [shot_page2] if not os.path.exists(path)]
assert len(missing_shots) == 0, f"스크린샷이 없습니다: {missing_shots}"

# TC-6-06. 기획서와 다른 값이 나와도 기대 목록을 화면 값으로 바꾸지 않습니다.
# 2페이지 첫 행 · 겹친 닉네임 · 빠진 닉네임을 한 메시지에 적으면,
# 보고를 받는 사람이 어느 페이지의 시작 위치가 어긋났는지 알 수 있습니다
assert joined == SPEC_RANKING, (
    f"랭킹 두 페이지를 이어 붙인 목록이 기획서 20명과 다릅니다. "
    f"2페이지 첫 행: 기대 11위 랭커11 62230, 실제 {page2[0]['rank']}위 {page2[0]['nick']} {page2[0]['score']} "
    f"(1페이지 마지막 10위 {page1[-1]['score']}보다 점수가 큽니다). "
    f"겹쳐 나온 닉네임: 기대 [], 실제 {duplicated}. "
    f"어느 페이지에도 없는 닉네임: 기대 [], 실제 {missing}")
