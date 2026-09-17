import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# 화면 구조
#
# <input type="text" id="keyword" name="q" placeholder="검색어를 입력하세요">
# <button id="search-btn" class="btn primary">검색</button>
# <div id="result-count">검색 결과: 0건</div>
#
# 동작: 검색 버튼을 누르면 result-count 의 텍스트가 즉시 바뀝니다.
#       "로그인"으로 검색하면 "검색 결과: 3건"이 됩니다.
# ────────────────────────────────────────────────

driver = webdriver.Chrome()
driver.get("http://localhost:8080")

# 1. 검색 입력창을 찾아 search_box 변수에 담으세요.
search_box = driver.find_element(By.ID, "keyword")

# 2. 검색 입력창에 "로그인"을 입력하세요.
search_box.send_keys("로그인")

# 3. 검색 버튼을 찾아 클릭하세요.
el_btn_search = driver.find_element(By.ID, "search-btn")
el_btn_search.click()

# 4. 결과 개수 문구를 읽어 count_text 변수에 담으세요.
el_result = driver.find_element(By.ID, "result-count")
count_text = el_result.text

print(count_text)

# 5. 검색 결과가 0건이 아닌지 검증하세요.
assert "0건" not in count_text, "검색 결과가 없습니다."

# 검색 결과: 0건

# split(":") ["검색 결과" , "0건"]
# [-1]
# replace("건","")
# int()



# snipet
# 자동완성