import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()



# selenium - 대기하기 위한 방법
# 암시적인 - driver.implicitly_wait
# 명시적인 - WebDriverWait



# 암시적인 대기 <- 일단 기다리겠다.
# 5초동안은 기다리겠다.
# 5초를 계속 기다리는게 아니라,
# 0.5초 마다 요소가 있는지 확인
#  -> 아직까지 없으면 계속 기다리고
#  -> 요소를 찾았다면 더이상 기다리지 않고 다음코드로 넘어감
# 5초 동안 못찾았다면 -> NoSearchException
# driver.implicitly_wait(5)


driver.get("https://302lab.co.kr/websample/selenium-demo/02_%EB%93%9C%EB%A1%AD%EB%8B%A4%EC%9A%B4")

# time.sleep(1) # <- 필요가 없음, get 이후 시간을 보장

el_input_player = driver.find_element(By.ID, "player-input")
el_input_player.send_keys("아르")
el_input_player.send_keys(Keys.ENTER)

# 시간을 짧게 설정 - 데이터 불러오기 전에 처리
# 시간을 길게 설정 - 시간 낭비
# time.sleep(5) # <- 필요 함, 검색후 데이터가 오기까지 0.8초 걸리고, 이후 부터 클래스 활용이 가능

# wait - 기다림 기능이 있는 객체
# 명시적인 wait
# 조건 
# ★★★ - 기본적으로 활용가능 [web element]
# - presence_of_element_located : 찾으려고 하는 한개의 데이터가 presence 할때까지
# - visibility_of_element_located : 찾으려고 하는 element가 visible 상태가 될때까지  - is_display
# - element_to_be_clickable : 찾으려고 하는 element가 클릭이 가능할때까지 - is_enabled

# ★★ - 자주 쓰이지만 상황이 정해져 있을 때
# - presence_of_all_elements_located : 찾으려고 하는 여러개의 데이터가 모두 presence 할때까지 [web element - list]
# - invisibility_of_element_located : 사라질때 까지 기다린다. -> 로딩바, 스피너  
# - text_to_be_present_in_element : 결과 문구에 글자가 들어올때까지

# ★ - 특정 상황에서만 쓰이는 것들
# - text_to_be_present_in_element_value : 입력칸에 특정 글자가 들어올떄까지
# - alert_is_present : alert, confirm 창이 활성화 될 때
# - number_of_windows_to_be : 특정한 갯수만큼 창이 뜨는 경우

wait = WebDriverWait(driver, 10)
wait.until(
    EC.number_of_windows_to_be((By.CLASS_NAME, "player-item"))
    )


el_player_item = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "player-item"), 
            "찾으려는 아이템이 없습니다.")
    )


# el_option_players = driver.find_elements(By.CLASS_NAME, "player-item")
# print(len(el_option_players))




input()