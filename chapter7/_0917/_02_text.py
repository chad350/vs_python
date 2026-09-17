import time
import re
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Chrome()

driver.get("https://302lab.co.kr/websample/selenium-advanced-demo/a02_notice_cleanup")

el_title = driver.find_element(By.ID, "notice-title")

# element 를 얻게 되면 문자열이 나오는데
# 형식이 우리가 다를 수가 있음
text = el_title.text
content = el_title.get_attribute("textContent")

# repr 원본 실제로 어떻게 구성되어 있는지 확인
print("text ",repr(text))
print("content ",repr(content))


# 원하는 값이 될 수 있도록 가공
result = content.split()
print(result)

result = " ".join(result)
print(result)


assert result == "[점검] 9월 정기 점검 안내", "title 설정에 문제가 있습니다."
print("title 이 잘 설정되었습니다!!")


# 숫자 X,  문자 O
# 표시 자체는 문제가 없는데, 비교나 계산이 불가능
# 원화 - ₩1,299
# 달러 - $4.99
el_price_krw = driver.find_element(By.ID, "price-krw")
print(el_price_krw.text)

price_krw_value = int(el_price_krw.text.replace("₩","").replace(",",""))
print(price_krw_value * 2)

# 정규식                   ₩1,299
#                  re.함수(  )
#                  re.sub( 패턴 ,   바꿀 대상  ,  대상이될 문자  )
# regex_krw_value = re.sub(r"[^0-9]", "", el_price_krw.text)
regex_krw_value = int(re.sub(r"[^0-9]", "", el_price_krw.text))
print("정규식 버전 : ", regex_krw_value)

# 문자열 맨 앞에서 검에서 검사 
패턴 = r"[0-9]+"
대상문자열 = el_price_krw.text
치환문자 = ""

re.sub(패턴, 치환문자 , 대상문자열) # 전체에서 일치하는 하는 것을 찾아서 치환

re.findall(패턴, 대상문자열) # 전체에서 일치하는 것 전부

re.search(패턴, 대상문자열)  # 전체 중에서 일치하는 첫번째 요소

re.match(패턴, 대상문자열) # 맨 앞에 데이터가 패턴으로 시작하는지
re.fullmatch(패턴, 대상문자열)




el_price_usd = driver.find_element(By.ID, "price-usd")
print(el_price_usd.text)

price_usd_value = float(el_price_usd.text.replace("$", ""))
print(price_usd_value * 2)

regex_usd_value = float(re.sub(r"[^0-9]", "", el_price_usd.text))
print("정규식 버전 : ", regex_usd_value)


el_notice_time = driver.find_element(By.ID, "notice-time")
print(el_notice_time.text)


date = re.findall( r"[0-9]+" , el_notice_time.text)
print("[0-9] : ", date)

date2 = re.findall( r"\d+" , el_notice_time.text)
print("\\d : ",date2)

#                    2-5-5
date = re.search(r"(\d+)-(\d+)-(\d+)", el_notice_time.text)
print(date.group(0))
print(date.group(1))
print(date.group(2))
print(date.group(3))

time_re = re.search(r"(\d+):(\d+)", el_notice_time.text)
print(time_re.group(0))
print(time_re.group(1))
print(time_re.group(2))

time_re = re.search(r"\d+:\d+ ~ \d+:\d+", el_notice_time.text)
print(time_re)



el_list_reward = driver.find_element(By.ID, "reward-list")
print(el_list_reward.text)

# findall -> 정수
print(repr(re.findall(r"\d+", el_list_reward.text)))

# findall -> 정수 ,
found = re.findall(r"[0-9,]+"  , el_list_reward.text)
print("숫자가 포함된 모든것을 체크한 리스트")
print(found)

#  0        1       2        3        4   
# 1,000  /  ,  /   500  /    ,   /   2,000
numbers = [s for s in found if s != "," ]       # print(", 를 제외한 리스트")
amount = [s.replace("," , "") for s in numbers] # print("숫자에서 , 를 제외한 리스트")
amount = [int(s) for s in amount]               # print("문자를 숫자로 변환한 리스트")

rusult = [ int(s.replace("," , "")) for s in found if s != "," ]
print(rusult)

stock = "재고 12개 남음"

# 정규식 X
stock_count = stock.split()
print(stock_count)

new_el = []
for el in stock_count:
    s = el.rstrip('개')     
    if s.isdigit() :
        new_el.append(s)

print(new_el)

new_el_2 = [el.rstrip('개') for el in stock_count if el.rstrip('개').isdigit()]
print(new_el_2)


# 정규식 O
stock = re.findall(r"\d+" , stock)
print(stock)




input()