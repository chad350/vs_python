drops = ["포션", "가죽 조각", "포션", "이끼", "가죽 조각", "포션", "룬 조각", "이끼"]
kinds = set(drops) # ["포션", "가죽 조각", "이끼", "룬 조각"]

total_len = len(drops)
kind_len = len(kinds)

max_count = 0
max_item = ""

print("[드랍 결과]")
print("전체", total_len , "개 / 종류" , kind_len , "종")
for item in kinds :
    item_count = drops.count(item)
    print(item ,":", item_count,"개")

    if(item_count > max_count) :
        max_count = item_count
        max_item = item

print("가장 많이 나온 것:", max_item, max_count ,"개")

#숫자 len count

# [드랍 결과]
# 전체 8 개 / 종류 4 종
# 가죽 조각 : 2개
# 룬 조각 : 1개
# 이끼 : 2개
# 포션 : 3개

# 가장 많이 나온 것: 포션 3 개  [선택사항]
