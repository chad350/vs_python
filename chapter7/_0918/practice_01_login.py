""" 실습 1 시작 코드 · 로그인 실패 3가지와 쿠키로 로그인 상태 확인 """
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

SITE = "https://302lab.co.kr/websample/game-site"       # 로컬 서버로 실습할 때는 "http://localhost:8640"


driver = webdriver.Chrome()
wait = WebDriverWait(driver, 5)

def login(id, pw):
    email_box = driver.find_element(By.ID, "login-email")
    email_box.clear()
    email_box.send_keys(id)

    pw_box = driver.find_element(By.ID, "login-pw")
    pw_box.clear()
    pw_box.send_keys(pw)

    wait.until(
        EC.element_to_be_clickable((By.ID, "login-btn"))
    ).click()



# wait.until(EC.text_to_be_present_in_element((By.ID, "login-error"), "올바르지 않습니다"), message="오류 문구가 나타나지 않음")
# cookie = driver.get_cookie("mg_session")                      # 없으면 None
# driver.delete_cookie("mg_session")
# driver.add_cookie({"name": "mg_session", "value": saved})     # 사이트 화면이 열려 있을 때만 쓸 수 있음
# wait.until(EC.url_contains("/login"), message="로그인 화면으로 이동하지 않음")


# 미션 1. 로그인하지 않은 상태에서 브라우저로 인벤토리 주소 inventory.html?reset=1 을 엽니다.
#   확인하려는 것: 로그인이 필요한 화면이 로그인 화면으로 이동하고, 돌아갈 화면을 주소에 남기는지
#   실패 처리: 로그인 화면으로 5초 안에 이동하지 않으면 TimeoutException 으로 멈춥니다.
#   판단 기준: 주소에 /login 과 next=inventory 가 있음

#   필요한 아이디어
#     ① driver.get 으로 inventory.html?reset=1 열기 (reset=1 은 처음 상태로 되돌리고 쿠키도 지움)
#     ② 로그인 화면으로 이동하는 것은 화면 스크립트가 하므로 바로 읽지 말고 EC.url_contains("/login") 으로 대기
#     ③ 302lab 서버는 .html 을 지우므로 주소 판단은 "login.html" 이 아니라 "/login" 으로
#     ④ driver.current_url 을 변수에 저장해 두고 마지막 assert 에서 "next=inventory" 확인

driver.get(SITE + "/inventory.html?reset=1")
wait.until(
    EC.url_contains("/login"), 
    "로그인하지 않았는데 인벤토리가 열림"
)
first_url = driver.current_url
print("처음 이동한 주소:", first_url)




# 미션 2. 로그인 화면에서 실패 경우 3가지(빈 이메일, 틀린 비밀번호, 대문자 이메일 ARTIA@MOON.GG)를 반복문 하나로 입력하고, 경우마다 (경우 이름, 오류 문구, 로그인 화면에 머물렀는지) 를 리스트에 기록합니다.
#   확인하려는 것: 잘못된 로그인 3가지가 모두 거절되는지
#   실패 처리: 오류 문구가 5초 안에 나타나지 않으면 경우 이름이 들어간 메시지와 함께 TimeoutException 으로 멈춥니다.
#   판단 기준: 3가지 모두 오류 문구가 나타나고 주소에 /login 이 남아 있음

#   필요한 아이디어
#     ① 실패 경우 3가지를 (이름, 이메일, 비밀번호) 튜플의 리스트로 만들기
#     ② for title, email, password in cases: 로 순회
#     ③ 순회할 때마다 이메일·비밀번호 칸을 clear() 로 비운 뒤 send_keys (안 비우면 앞 글자 뒤에 이어서 입력됨)
#     ④ 로그인 버튼은 누른 뒤 0.8초 동안 비활성 → EC.element_to_be_clickable 로 대기 후 click
#     ⑤ 오류 문구는 0.8초 뒤에 나타남 → EC.text_to_be_present_in_element((By.ID, "login-error"), "올바르지 않습니다") 로 대기
#     ⑥ (경우 이름, 오류 문구 .text, "/login" in driver.current_url) 튜플을 리스트에 append

cases = [
    ("빈 이메일", "", "artia2026"),
    ("틀린 비밀번호", "artia@moon.gg", "wrong0000"),
    ("대문자 이메일", "ARTIA@MOON.GG", "artia2026")
]

failures = []

for title, email, password in cases:

    # 코드가 복잡해 질때 단순화
    login(email, password)

    wait.until(
        EC.text_to_be_present_in_element((By.ID, "login-error"), "올바르지 않습니다"),
        f"{title}: 오류 문구가 나오지 않음"
    )

    el_error = driver.find_element(By.ID, "login-error")

    failures.append((title, el_error.text, "/login" in driver.current_url))

for f in failures:
    print(f)





# 미션 3. 올바른 계정 artia@moon.gg / artia2026 으로 로그인하고, 브라우저가 인벤토리 화면으로 돌아오면 쿠키 mg_session 값을 변수에 보관합니다.
#   확인하려는 것: 로그인한 뒤 처음 열려던 화면으로 돌아오는지
#   실패 처리: 인벤토리 화면으로 5초 안에 돌아오지 않으면 TimeoutException 으로 멈춥니다.
#   판단 기준: 주소에 /inventory, 닉네임 「아르티아」, 쿠키 값이 MG- 로 시작
#   필요한 아이디어
#     ① 이메일 칸에 앞 경우의 글자가 남아 있음 → 두 칸 모두 clear() 후 올바른 계정 입력
#     ② 로그인 성공 뒤 인벤토리로 돌아오는지 EC.url_contains("/inventory") 로 대기
#     ③ 닉네임은 EC.visibility_of_element_located 로 대기한 뒤 .text
#     ④ driver.get_cookie("mg_session") 은 쿠키가 없으면 None → cookie["value"] if cookie else "" 로 값 보관


login("artia@moon.gg", "artia2026")

wait.until(
    EC.url_contains("/inventory"), 
    message="로그인한 뒤 인벤토리로 돌아오지 않음"
)

nick = wait.until(
    EC.visibility_of_element_located((By.ID, "nav-nick")), 
    "로그인 뒤 닉네임이 보이지 않음"
).text

cookie = driver.get_cookie("mg_session")
saved = cookie["value"] if cookie else ""

print("로그인 뒤 주소:", driver.current_url, "/ 닉네임:", nick, "/ 쿠키:", saved)



# 미션 4. 쿠키를 3가지 상태로 바꾸며 인벤토리 화면을 엽니다. ① 쿠키를 지우고 새로고침 ② 가짜 쿠키 FAKE-0000 을 넣고 인벤토리 주소 열기 ③ 보관한 쿠키를 넣고 인벤토리 주소 열기
#   확인하려는 것: 사이트가 쿠키 이름뿐 아니라 쿠키 값까지 확인해서 로그인 상태를 판단하는지
#   실패 처리: 각 상태에서 기대한 화면이 5초 안에 나타나지 않으면 TimeoutException 으로 멈춥니다.
#   판단 기준: ①·②는 로그인 화면으로 이동, ③은 인벤토리 화면과 닉네임 「아르티아」

#   필요한 아이디어
#     ① 쿠키 삭제: driver.delete_cookie("mg_session") → driver.refresh() → EC.url_contains("/login") 대기 → 주소 저장
#     ② 가짜 쿠키: driver.add_cookie({"name": "mg_session", "value": "FAKE-0000"}) → 인벤토리 주소 열기 → "/login" 대기 → 주소 저장
#     ③ 진짜 쿠키: 미션 3 에서 보관한 값으로 add_cookie → 인벤토리 주소 열기 → 닉네임 대기 → 주소 저장
#     ④ add_cookie 는 사이트 화면이 열려 있을 때만 쓸 수 있음
#     ⑤ 주소 3개는 변수에 저장해 두고 마지막에 한꺼번에 assert


driver.delete_cookie("mg_session")
driver.refresh()

wait.until(
    EC.url_contains("/login"), 
    "쿠키를 지웠는데 로그인 화면으로 이동하지 않음"
)

deleted_url = driver.current_url

driver.add_cookie({"name": "mg_session", "value": "FAKE-0000"})
driver.get(SITE + "/inventory.html")

wait.until(
    EC.url_contains("/login"), 
    "가짜 쿠키로 인벤토리가 열림"
)

fake_url = driver.current_url

driver.add_cookie({"name": "mg_session", "value": saved})
driver.get(SITE + "/inventory.html")

restored_nick = wait.until(
    EC.visibility_of_element_located((By.ID, "nav-nick")),
    "보관한 쿠키를 넣었는데 로그인 상태가 아님"
).text

restored_url = driver.current_url

print("쿠키 삭제 뒤:", deleted_url)
print("가짜 쿠키 뒤:", fake_url)
print("쿠키 복원 뒤:", restored_url, "/ 닉네임:", restored_nick)



driver.quit()

# ── 검증 (판단 결과를 출력한 뒤 assert 합니다)
assert "next=inventory" in first_url, f"돌아갈 화면 정보가 없음: {first_url}"
assert nick == "아르티아" and saved.startswith("MG-"), f"닉네임 {nick} / 쿠키 {saved}"
assert "/login" in deleted_url and "/login" in fake_url, f"삭제 뒤 {deleted_url} / 가짜 쿠키 뒤 {fake_url}"
assert "/inventory" in restored_url and restored_nick == "아르티아", f"복원 뒤 {restored_url} / {restored_nick}"