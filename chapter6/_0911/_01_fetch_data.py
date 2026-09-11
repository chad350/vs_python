import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("https://302lab.co.kr/websample/selenium-demo/01_%EA%B0%92%EC%9D%BD%EA%B8%B0_%EA%B2%80%EC%A6%9D")

first_title = driver.find_element(By.CSS_SELECTOR, "#search h2")
print(first_title.text)      # 내부 텍스트를 문자열로
print(first_title.tag_name)  # 태그 값

section_search = driver.find_element(By.CSS_SELECTOR, "#search")
print(section_search.text)   # 내부 Tag 들을 전부 체크해서 각각의 값을 하나의 문자열

# 속성 체크
input_search = driver.find_element(By.ID, "q")
print(input_search.get_attribute("id"))
print(input_search.get_attribute("type"))
print(input_search.get_attribute("value"))
print(input_search.get_attribute("placeholder"))

search_text = input_search.get_attribute("value")
print("search :",search_text)

input_search.send_keys("test-id")

# 초기값 설정 되어 있을때는 <-   
print(input_search.get_attribute("value"))
print(input_search.get_attribute("placeholder"))

# 초기값이 변경된 것 을 감지하지 하지 못할때 같이 고려 -> checkbox 의  checked 등
print(input_search.get_property("value"))
print(input_search.get_property("placeholder"))


span_level = driver.find_element(By.ID, "level")
level = int(span_level.text)  # 가지고 온 값은 "문자!!" - 계산이 필요하다면 "숫자로 바꿔서 연산"

check_nickname = "아르티아"
txt_nickname = driver.find_element(By.ID, "nickname")

#         42
# assert  조건   , "문장"
assert 40 <= level, "플레이어 레벨이 40을 안됩니다."
assert txt_nickname.text == check_nickname , f"체크하려는 아이디가 {check_nickname}가 아닙니다."

# <a id="log-link" href="/players/1024/logs">접속 기록 보기</a>
log_link = driver.find_element(By.ID, "log-link")
print(log_link.get_attribute("href"))   # https://302lab.co.kr/players/1024/logs
print(log_link.get_dom_attribute("href")) # /players/1024/logs

# style 중에서 display 가 none 설정되면 text 정보를 읽을 수가 없다.
note = driver.find_element(By.ID, "hidden-note")
print(note.id)
print(note.tag_name)
print(note.text)  # <- X
print(note.get_attribute("textContent"))  # <- 숨겨져 있는 텍스트도 추출 가능


# Data Check
# 해당 요소가 숨겨져 있는지 체크
if not log_link.is_displayed():
    print("log_link 요소가 숨겨져 있습니다.")

if not note.is_displayed():
    print("note 요소가 숨겨져 있습니다.")


# 해당 버튼들이 선택이 되어 있는지
check_push = driver.find_element(By.ID, "agree-push")
check_mail = driver.find_element(By.ID, "agree-mail")
if not check_push.is_selected():
    check_push.click()

if not check_mail.is_selected():
    check_mail.click()

# 해당 버튼들이 사용할 수 있는 상태인지 
radio_vip = driver.find_element(By.ID, "grade-vip")
radio_staff = driver.find_element(By.ID, "grade-staff")

if radio_vip.is_enabled():
    radio_vip.click()
else:
    print("radio_vip 은 선택할 수 없습니다.")

if radio_staff.is_enabled():
    radio_staff.click()
else:
    print("radio_sttaf 은 선택할 수 없습니다.")



input() 