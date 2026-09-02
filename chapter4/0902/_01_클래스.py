# 소모품
# 속성(정보) - 이름, 가격
# 기능(행동) - 사용, 판매
class Consumalble:

    # 속성을 추가할떄는??? -> 생성자
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def use(self):
        print(f"{self.name} 아이템을 사용했습니다.")
        print("체력을 회복했습니다.")

    def sell(self):    
        print(f"아이템을 판매했습니다. {self.price} G 획득했습니다.")


# 체력물력, 마나물량
item = Consumalble("체력물력", 100)
item.use()
item.sell()


item2 = Consumalble("마나물량", 150)
item2.use()
item2.sell()


