import csv

f = open("items.csv", encoding="utf-8")
reader = csv.DictReader(f)

# {'item_id': 'IT1001', 'name': '낡은 단검', 'type': '무기', 'grade': 'COMMON', 'level_limit': '1', 'attack_power': '5', 'obtain_location': '초보자 마을'}
# 조건문, 반복문, 딕셔너리 

# 초보자 마을 상점의 아이템 print
print("[초보자 마을 아이템]")
# for item in reader:
#     location = item["obtain_location"]
#     if location in "초보자 마을":
#         print(item["name"])

# 레벨제한이 10 이하인 아이템 print
# 10 이하??? <- 숫자이어야한다
print("[10레벨 이하 아이템]")
# for item in reader:
#     level_limit = int(item["level_limit"])
#     if level_limit <= 10 :
#         print(item["name"])

# 무기들의 공격력 합쳐서 print
print("[무기들의 합계]")
total = 0
for item in reader:
    item_type = item["type"]
    if item_type == "무기":
        atk = int(item["attack_power"])
        total += atk

print(f"무기 공격력 합계는 {total}입니다")


f.close()