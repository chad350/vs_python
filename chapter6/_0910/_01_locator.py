import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("https://302lab.co.kr/websample/css-selector/")

# id - 유니크함 보장되기 때문에 일단 존재하면 가장 먼저 고려할 요소
# driver.find_element(by = By.ID, value = "loginBtn")
login_btn = driver.find_element(By.ID ,"btn_login_7a3f")
input_pw = driver.find_element(By.ID ,"user_pw_7a3f")
print(login_btn.text)

# tag - 대부분 페이지에 tag 는 여러개 존재 
title = driver.find_element(By.TAG_NAME, "h1")
print(title.text)
btn = driver.find_elements(By.TAG_NAME, "button")
print(btn[1].text)

# name - 폼데이터를 대상으로 유효한 옵션
keyword = driver.find_element(By.NAME, "keyword")
print(keyword.text)
print(keyword.tag_name)
print(keyword.id)

# class - 중복된 대상이 여럿 있을때 특정 정보를 추출
items = driver.find_elements(By.CLASS_NAME, "item")
print(f"{len(items)} 개 의 아이템을 찾았습니다.")

for item in items:
    item_part = item.text.split("\n")
    print(f"[{item_part[0]}] {item_part[1]} - 가격 : {item_part[2]}")


# link text - 링크로 연결(a 태그) 데이터를 찾을때 정확하게 이름이 매칭되는 경우 활용
doc_1 = driver.find_element(By.LINK_TEXT, "설명서")  # 검색 결과 : 1
# doc_2 = driver.find_element(By.LINK_TEXT, "문서")   # 검색 결과 : 0 - 에러
print(doc_1.text)


# partial link text - 링크로 연결(a 태그) 데이터를 찾을때 이름이 포함되는 경우 활용
docs_1 = driver.find_elements(By.PARTIAL_LINK_TEXT, "설명서")   # 검색 결과 : 2
docs_2 = driver.find_elements(By.PARTIAL_LINK_TEXT, "문서")   # 검색 결과 : 2

print(f"설명서 찾은 것 : {len(docs_1)}개")
for idx, doc in enumerate(docs_1, start=1):
    print(f"{idx} : {doc.text}")

print(f"문서 찾은 것 : {len(docs_2)}개")
for idx, doc in enumerate(docs_2, start=1):
    print(f"{idx} : {doc.text}")


# css_selector - 원하는 조건이 복잡할때 조금 더 유연하게 검색하는 방법
title_by_css = driver.find_element(By.CSS_SELECTOR, "h1")
login_by_css = driver.find_element(By.CSS_SELECTOR, "#btn_login_7a3f")
item_by_css = driver.find_elements(By.CSS_SELECTOR, ".item")

print(title_by_css.text)
print(login_by_css.text)
print(f"item 갯수 : {len(item_by_css)}개")

# 속성 - 시작 / 끝 / 포함관계 체크
search_btn = driver.find_element(By.CSS_SELECTOR, "[data-testid='search-submit']")
start_user = driver.find_elements(By.CSS_SELECTOR, "[id^='user']") # user 로 시작하는 id
end_7a3f = driver.find_elements(By.CSS_SELECTOR, "[id$='_7a3f']") # _7a3f 로 끝나는 id
contain_email = driver.find_elements(By.CSS_SELECTOR, "[id*='email']") # email 이 포함된 id

print(search_btn.text)
print(f"user 로 시작하는 갯수 : {len(start_user)}개")
print(f"_7a3f 로 끝나느 갯수 : {len(end_7a3f)}개")
print(f"email 로 포함하는 갯수 : {len(contain_email)}개")

# 부모 자식 포함관계를 찾을 수 있다.
# 조건1 조건2   <- 사이에 띄어쓰기 : 자손 중에서 체크
products = driver.find_elements(By.CSS_SELECTOR, "#productList li")
badge = driver.find_elements(By.CSS_SELECTOR, "#productList span")
print(f"프로덕트 갯수 : {len(products)}")
print(f"뱃지 갯수 : {len(badge)}")

# 조건1 > 조건2   <- 사이에 > : 자식 중에서 체크
products_2 = driver.find_elements(By.CSS_SELECTOR, "#productList > li")
badge_2 = driver.find_elements(By.CSS_SELECTOR, "#productList > span")
print(f"프로덕트 갯수 : {len(products_2)}")
print(f"뱃지 갯수 : {len(badge_2)}")


sales = driver.find_elements(By.CSS_SELECTOR, ".item.sale")
print(f"세일중인 아이템 갯수 : {len(sales)}")
for item in sales:
    print(item.text)








# xpath




input()