import csv

f = open("items.csv", encoding="utf-8")

# 결과 - 문자열 리스트
# ['item_id', 'name', 'type', 'grade', 'level_limit', 'attack_power', 'obtain_location']
# ['IT1001', '낡은 단검', '무기', 'COMMON', '1', '5', '초보자 마을']
# ['IT1002', '녹슨 장검', '무기', 'COMMON', '3', '8', '초보자 마을']
# reader = csv.reader(f)
# for row in reader:
#     print(row)

# 결과 - 딕셔너리
# {'item_id': 'IT1001', 'name': '낡은 단검', 'type': '무기', 'grade': 'COMMON', 'level_limit': '1', 'attack_power': '5', 'obtain_location': '초보자 마을'}
# {'item_id': 'IT1002', 'name': '녹슨 장검', 'type': '무기', 'grade': 'COMMON', 'level_limit': '3', 'attack_power': '8', 'obtain_location': '초보자 마을'}
# {'item_id': 'IT1003', 'name': '나무 활', 'type': '무기', 'grade': 'COMMON', 'level_limit': '1', 'attack_power': '4', 'obtain_location': '초보자 마을'}
reader_dict = csv.DictReader(f)
for dict in reader_dict:
    print(dict)


f.close()