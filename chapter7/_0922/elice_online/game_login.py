"""엘리스 온라인 실습 제공 코드 · 로그인까지 끝낸 브라우저를 만들어 줍니다.

로그인은 앞 수업에서 다뤘으므로 실습에서 다시 만들지 않습니다.
이 파일을 실습 파일과 같은 폴더에 game_login.py 로 저장하고, 실습 파일을 이렇게 시작합니다.

    from game_login import setup, close_dialog, save_screenshot, GAME_URL

    driver, wait = setup()
    # 여기부터 실습 코드를 씁니다
    driver.quit()

이 파일도 실습 코드처럼 브라우저만 씁니다 (requests 를 쓰지 않습니다).
setup() 은 로그인 화면에서 로그인하고, 마이페이지의 「데이터 초기화」 를 누르고,
닉네임을 기본값으로 되돌려 매번 같은 상태에서 시작하게 합니다.
"""
import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# ======================================================================
# ★ 내 계정을 넣는 곳 ★
# 계정은 각자 가입해서 씁니다. 내가 쓸 아이디 · 비밀번호를 아래 따옴표 안에 넣습니다.
#   예) USERNAME = os.environ.get("GAME_ID", "kimqa01")
#       PASSWORD = os.environ.get("GAME_PW", "practice1234")
# 아직 가입하지 않았으면 setup() 이 처음 실행할 때 이 값으로 가입 화면에서 가입해 줍니다.
# 게임 화면(/signup)에서 직접 가입한 계정을 넣어도 됩니다.
# 가입 규칙: 아이디는 영문 소문자와 숫자 4~12자이고 다른 사람과 겹칠 수 없습니다.
#            비밀번호는 8자 이상입니다. 실제로 쓰는 비밀번호는 넣지 않습니다.
#            닉네임은 2~8자이고 다른 사람과 같아도 됩니다.
# 값을 고치지 않고 환경 변수(GAME_ID · GAME_PW · GAME_NICK)로 넘겨도 됩니다.
#   예) GAME_ID=kimqa01 GAME_PW=practice1234 python lab1_1_mypage_info.py
# ======================================================================
GAME_URL = os.environ.get("GAME_URL", "https://elice-game.fly.dev")   # 게임 주소 (보통 바꾸지 않습니다)
USERNAME = os.environ.get("GAME_ID", "duadpcks")                              # ★ 내 아이디
PASSWORD = os.environ.get("GAME_PW", "test123456")                              # ★ 내 비밀번호
NICKNAME = os.environ.get("GAME_NICK", "수련생")                       # 닉네임 (바꾸지 않아도 됩니다)
SHOT_DIR = os.environ.get("SHOT_DIR", "screenshots")                  # 스크린샷을 모을 폴더


def make_driver():
    """크롬 브라우저를 엽니다."""
    opts = Options()
    # 환경 변수 HEADLESS 가 있으면 창을 띄우지 않고 돌립니다. 진행을 눈으로 보려면 빼고 실행합니다
    if os.environ.get("HEADLESS"):
        opts.add_argument("--headless=new")
        opts.add_argument("--no-sandbox")
    # 창 크기를 고정해 화면 배치와 스크린샷 크기가 매번 같게 합니다
    opts.add_argument("--window-size=1280,900")
    return webdriver.Chrome(options=opts)


def make_wait(driver, seconds=15):
    """Explicit Wait 를 만듭니다. 기다리는 동안 요소가 없거나 만료되어도 끝내지 않고 다시 찾습니다."""
    # 기본 WebDriverWait 는 NoSuchElementException 만 무시합니다.
    # 인벤토리 · 퀘스트 · 경매장처럼 목록을 다시 그리는 화면에서는 찾은 직후 요소가 만료되어
    # .text 를 읽는 순간 StaleElementReferenceException 이 납니다.
    # 두 예외를 모두 넣어 두면 그 회차만 건너뛰고 다음 회차에 다시 찾습니다 (try/except 없이 같은 효과).
    return WebDriverWait(driver, seconds,
                         ignored_exceptions=(NoSuchElementException, StaleElementReferenceException))


def dialog_is_open(driver):
    """게임 Dialog(game-dialog)가 열려 있으면 True 를 돌려줍니다."""
    # find_elements 는 요소가 없으면 예외 대신 빈 목록을 돌려줍니다
    found = driver.find_elements(By.ID, "game-dialog")
    # 열림 여부는 글자가 아니라 <dialog> 의 open 속성으로 봅니다
    return bool(found) and found[0].get_attribute("open") is not None


def close_dialog(driver, wait):
    """구매 · 퀘스트 완료 · 전투 결과 뒤에 뜨는 Dialog 를 닫고 (제목, 본문) 을 돌려줍니다."""
    # 이 Dialog 는 showModal() 로 열려서, 열려 있는 동안 바깥 버튼을 누르면
    # ElementClickInterceptedException 이 납니다. 그래서 「열림 → 읽기 → 닫기 → 닫힘 확인」 을 한 번에 합니다
    wait.until(lambda d: dialog_is_open(d), message="Dialog did not open")
    title = driver.find_element(By.ID, "game-dialog-title").text          # 제목을 보관합니다 (예: 구매 완료!)
    message = driver.find_element(By.ID, "game-dialog-message").text      # 본문을 보관합니다
    driver.find_element(By.ID, "game-dialog-confirm").click()
    # 닫힌 것까지 확인해야 다음 버튼을 안전하게 누를 수 있습니다
    wait.until(lambda d: not dialog_is_open(d), message="Dialog did not close")
    return title, message


def save_screenshot(driver, name, el=None):
    """스크린샷을 SHOT_DIR/name.png 로 남기고 파일 경로를 돌려줍니다.

    el 을 넘기면 그 요소만 찍고, 넘기지 않으면 지금 보이는 화면 전체를 찍습니다.
    """
    # Selenium 은 폴더가 없으면 예외 없이 False 만 돌려주므로 폴더를 먼저 만듭니다
    os.makedirs(SHOT_DIR, exist_ok=True)
    path = os.path.join(SHOT_DIR, f"{name}.png")
    if el is None:
        saved = driver.save_screenshot(path)
    else:
        # 요소가 화면 밖에 있으면 잘려 찍히므로 화면 가운데로 스크롤한 뒤 요소만 찍습니다
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
        saved = el.screenshot(path)
    # 저장에 실패했으면 여기서 멈춰 알려 줍니다
    assert saved, f"screenshot was not saved: {path}"
    return path


def _login(driver, wait):
    """로그인 화면에서 로그인합니다. 성공하면 True, 계정이 없거나 비밀번호가 틀리면 False."""
    driver.get(GAME_URL + "/login")
    driver.find_element(By.ID, "li-username").send_keys(USERNAME)
    driver.find_element(By.ID, "li-password").send_keys(PASSWORD)
    # 로그인 버튼은 화면을 연 뒤 0.6초 동안 비활성입니다. 누를 수 있게 될 때까지 기다린 뒤 누릅니다
    wait.until(EC.element_to_be_clickable((By.ID, "li-submit")),
               message="login button never became clickable").click()
    # 성공하면 메인 화면(main-title)으로, 실패하면 로그인 화면에 남아 오류 문구(li-error)가 채워집니다.
    # or 로 두 조건을 이어 「둘 중 먼저 오는 것」 을 기다립니다. find_elements 는 없으면 빈 목록(거짓)입니다
    wait.until(lambda d: d.find_elements(By.ID, "main-title") or d.find_element(By.ID, "li-error").text,
               message="neither the main screen nor a login error appeared")
    # 기다림이 끝난 뒤 메인 제목이 있는지로 성공 · 실패를 가립니다 (try/except 대신 상태를 읽어 판단)
    return bool(driver.find_elements(By.ID, "main-title"))


def _signup(driver, wait):
    """가입 화면에서 계정을 만듭니다. 계정이 없을 때 처음 한 번만 쓰입니다."""
    driver.get(GAME_URL + "/signup")
    # (요소 id, 넣을 값) 쌍을 돌며 네 칸을 채웁니다
    for el_id, value in (("su-username", USERNAME), ("su-password", PASSWORD),
                         ("su-password2", PASSWORD), ("su-nickname", NICKNAME)):
        driver.find_element(By.ID, el_id).send_keys(value)
    # 가입 버튼은 닉네임 검사를 해야 켜집니다. 검사 결과는 1초 뒤에 옵니다
    driver.find_element(By.ID, "su-nick-check-btn").click()
    wait.until(lambda d: d.find_element(By.ID, "su-nick-result").text != "",
               message="nickname check on the sign-up screen did not answer")
    result = driver.find_element(By.ID, "su-nick-result").text
    assert result == "사용할 수 있는 닉네임입니다", f"sign-up nickname {NICKNAME!r}: {result}"
    driver.find_element(By.ID, "su-submit").click()
    # 성공하면 로그인 화면(li-signup-done), 실패하면 가입 화면(su-error)에 결과가 나옵니다.
    # 두 요소는 서로 다른 화면에 있어 find_element 로는 늘 한쪽에서 예외가 나므로,
    # find_elements 두 개를 이어 붙여 「글자가 있는 것이 하나라도 있으면」 끝냅니다
    wait.until(lambda d: any(el.text for el in d.find_elements(By.ID, "li-signup-done") + d.find_elements(By.ID, "su-error")),
               message="sign-up did not finish")
    errors = [el.text for el in driver.find_elements(By.ID, "su-error")]
    # 이미 있는 아이디라서 가입이 안 됐다면 로그인이 실패한 까닭은 비밀번호입니다
    hint = " The account exists, so GAME_PW is wrong." if errors and errors[0] == "이미 사용 중인 아이디입니다" else ""
    assert not errors, f"login failed, so tried to sign up, but: {errors[0] if errors else ''}.{hint}"


def _reset_on_my_page(driver, wait):
    """마이페이지의 「데이터 초기화」 를 누르고, 닉네임이 바뀌어 있으면 기본값으로 되돌립니다."""
    driver.get(GAME_URL + "/me")
    wait.until(EC.element_to_be_clickable((By.ID, "reset-btn")), message="My Page did not open")
    driver.find_element(By.ID, "reset-btn").click()
    # 누른 직후에는 결과가 아직 없습니다. 결과 문구가 정해진 글자가 될 때까지 기다립니다
    wait.until(lambda d: d.find_element(By.ID, "reset-msg").text == "데이터 초기화 완료",
               message="data reset did not finish")
    # 초기화는 닉네임을 되돌리지 않습니다. 실습 1-1 이 닉네임을 바꾸므로,
    # 되돌리지 않으면 두 번째 실행의 처음 값이 달라집니다. 바뀌어 있을 때만 되돌립니다
    if driver.find_element(By.ID, "me-nickname").text != NICKNAME:
        driver.find_element(By.ID, "nick-new").send_keys(NICKNAME)
        driver.find_element(By.ID, "nick-check-btn").click()
        wait.until(lambda d: d.find_element(By.ID, "nick-check-result").text != "",
                   message="nickname check did not answer")
        result = driver.find_element(By.ID, "nick-check-result").text
        assert result == "사용할 수 있는 닉네임입니다", f"nickname {NICKNAME!r}: {result}"
        driver.find_element(By.ID, "nick-save-btn").click()
        # 머리글 닉네임이 바뀐 것을 보고 끝났다고 판단합니다
        wait.until(EC.text_to_be_present_in_element((By.ID, "hdr-nick"), NICKNAME),
                   message="nickname was not restored to the default")


def setup(reset=True):
    """로그인하고 메인 화면에 선 브라우저를 (driver, wait) 로 돌려줍니다.

    reset=True 면 골드 · 인벤토리 · 퀘스트 · 입찰 · 출석을 처음 상태로 되돌리고 닉네임도 되돌립니다.
    reset=False 로 부르면 앞 실행에서 남은 값을 그대로 두고 볼 수 있습니다.
    """
    # 아이디 · 비밀번호를 넣지 않았으면 브라우저를 열기 전에 알려 줍니다
    assert USERNAME and PASSWORD, "game_login.py 맨 위 「내 계정을 넣는 곳」 의 USERNAME · PASSWORD 에 내 아이디 · 비밀번호를 넣으세요"
    driver = make_driver()
    wait = make_wait(driver)
    # 로그인이 안 되면(계정이 없으면) 가입한 뒤 한 번 더 로그인합니다
    if not _login(driver, wait):
        _signup(driver, wait)
        assert _login(driver, wait), "login failed after sign-up (check GAME_ID and GAME_PW)"
    if reset:
        _reset_on_my_page(driver, wait)
    # 마지막에 메인 화면에서 끝내, 모든 실습이 같은 화면에서 시작하게 합니다
    driver.get(GAME_URL + "/main")
    wait.until(EC.presence_of_element_located((By.ID, "main-title")), message="main screen did not open")
    return driver, wait