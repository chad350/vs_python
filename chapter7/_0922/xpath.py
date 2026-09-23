from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = "https://302lab.co.kr/websample/xpath-practice/x01_guild"

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 5)


driver.find_element(By.ID)
driver.find_element(By.CLASS_NAME)
driver.find_element(By.TAG_NAME)
driver.find_element(By.NAME)

driver.find_element(By.LINK_TEXT)
driver.find_element(By.PARTIAL_LINK_TEXT)

driver.find_element(By.CSS_SELECTOR)

# 요 친구
driver.find_element(By.XPATH)
# 화면에 보이는 글자로 검색
# 부모 요소를 접근

# 속성을 기준으로 접근할때 기본 값
# 1   2     3  
# //태그이름[@data-id='속성데이터']

# 1
# //  <-  [자손] 문서 하단 어디든
# /   <-  [자식] 문서 바로 밑에 있는 요소 중

# 2 
# 태그네임   * [모든 태그]  p  h1  div  span   li

# 3
# 조건 - 대괄호 하고 나서
# @ 가 들어가면 속성값을 체크를 하겠다.
# <li class="quest" data-qid="Q-101" data-state="done">    
# [@data-qid="Q-101]
# [@data-state="done"]



# 0. / 와 // 의 차이   ★★★
# // [자손]
# /  [자식]

# //li           문서에 있는 모든 li
# //ul/li        부모가 ul 인 li
# //section/h2   section 바로 아래에 있는 h2

# //*[@id='memberList']/li        목록의 바로 아래 자식 li
# //*[@id='memberList']//button    목록의 바로 아래 자식 li



# 1. 속성을 하나 대상으로 체크    
# //li[@data-role='member']         data-role 속성이 member 인 li
# //li[@data-role]                  data-role 속성이 있기만 한 li
# //*[@data-role]                   data-role 속성이 있기만 한 모든 요소
# //button[@disabled]               비활성화된 버튼
# //button[not(@disabled)]          활성화된 버튼
# //input[@placeholder='닉네임 검색']  안내글자에 닉네임 검색이라고 있는것
# //a[@href='#quests']              링크 주소라 quests 인 것

# 속성이 2개인 경우
# //li[@data-role='member'][@data-level>50]         2개 조건이 만족 해야함
# //li[@data-role='member' and @data-level>50]      2개 조건이 만족 해야함
# //li[@data-role='member' or @data-role='master']  2개 중 하나만 만족해도 됨
# //li[not(@data-role='master')]                    길드장이 아닌 것
# //li[@data-role][not(@data-role='master')]        역할 속성이 있으면서 길드장이 아닌 것
# //li[@data-state='done']/button[not(@disable)]    상태가 완료인 퀘스트가 가지고 있는 버튼(비활성화가 아닌것)
# //li[@data-state!='done']/button[@disable]        상태가 완료가 안된 퀘스트가 가지고 있는 버튼(비활성화)

# 숫자를 비교할 수 있음 - 비교  ★★
# //li[@data-level>50] 
# //li[@data-level>=50] 
# //li[@data-level<50] 
# //li[@data-level!=50] 

# 텍스트를 비교해서 검색   ★★★
# //span[text()='안개꽃']               element 안의 글자를 확인
# //span[normalize-space()='안개꽃']    element 와 자식까지 합쳐서 글자를 확인
# //span[contains()]                  글자가 포함되는 경우

# contains 
# //a[contains(text(),'퀘스트')]        a 를 찾는데 글에 퀘스트가 포함된 요소를 찾겠다.    [길드 퀘스트]
# //a[starts-with(text(),'길드')]       a 를 찾는데 글의 시작 길드    [길드원, 길드 퀘스트, 길드 규칙]


# 2. 순서 / 개수 확인
# [n]
# position()
# last()


# //*[@id='memberList']/li  
# //*[@id='memberList']/li[1]         첫번째가 1부터
# //*[@id='memberList']/li[2]
# //*[@id='memberList']/li[3]
# //*[@id='memberList']/li[Last()-1]  뒤에서 2번쨰
# //*[@id='memberList']/li[Last()]    위치가 맨뒤


# //*[@id='memberList']/li[potion()<=2]  순서가 2 이하인것
# //*[@id='memberList']/li[potion()>4]   순서가 4 보다 뒤에 있는 것



# 3. 부모와 조상한테 접근
# 바로 쓰는 것보다 요소를 하나 찾은 다음에 상단으로 접근
# /..               부모
# /parant::div      부모가 div 인 경우
# /parant::li       부모가 li 인 경우

# /../..            부모의 부모
# ancestor::li      조상가운데 li 전부
# ancestor::*       조상 전부
# ancestor::*[1]    가장 가까운 조상
# ancestor::*[2]    두번째로 가까운 조상
# ancestor::section 조상가운데 section