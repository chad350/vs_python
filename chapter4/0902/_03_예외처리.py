# 소모품
# 속성(정보) - 이름, 가격
# 기능(행동) - 사용, 판매
class Consumalble:
    # 속성을 추가할떄는??? -> 생성자
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def use(self):
        print(f"{self.name} 아이템을 사용했습니다!!!!")

    def sell(self):    
        print(f"아이템을 판매했습니다. {self.price} G 획득했습니다.")


class ManaPotion (Consumalble) : 
    def __init__(self, name, price, amount):
        super().__init__(name, price)


        # 숫자
        # 방법 1. 타입 체크 -> 불가하다면 넘어가도록 -> return

        # isinstance
        # 허용하는 경우만 진행
        if type(amount) is int :    
            self.amount = amount  

        # 허용되지 않으면 return
        if type(amount) is not int :    
            return

        # 방법 2. 타입 체크 -> 불가하다면 에러 발생
        # 허용되지 않으면 예외처리
        if type(amount) is not int :    
            raise Exception("숫자가 아닙니다.")
            
        self.amount = amount  


    def use(self):
        super().use()
        print(f"MP 를 회복합니다   회복량 : {self.amount}")

    def check(self) :
        print("마나포션을 사용할 수 있습니다.")


class HealPotion (Consumalble) : 
    def use(self):
        super().use()
        print("HP 를 회복합니다")



tmp = ManaPotion("테스트 물약", 100, "50")
tmp.use()


print(vars(tmp))



print()



print("Consumalble Class")
item1 = Consumalble("아이템", 100)
item1.use()
item1.sell()


print()
print("ManaPotion Class")

item2 = ManaPotion("MP 물약", 150, 20)
item2.use()
item2.sell()
item2.check()

print()
print("HealPotion Class")

item3 = HealPotion("HP 물약", 150)
item3.use()
item3.sell()