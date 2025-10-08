class Item():
    def __init__(self, name:str, price:float, quantity = 0):
        self.name = name
        self.price =price
        self.quantity = quantity

        assert quantity >= 0
        assert  price >=0
    def Tong_Gia(self):
        return  self.price  *self.quantity

    @staticmethod
    def CheckGia(gia):
        if gia<=500:
            return "So Cheap, dat o tang 1"
        else:
            return "Expensive, dat o tang 2"

class Phone(Item):
    def __init__(self, name:str, price:float, quantity = 0, type ="4G"):
        super().__init__(name, price, quantity)
        self.type = type

phone1 = Phone("SamSung",10000, 2,"5G")
phone2 = Phone("Iphone", 30000, 3, "5G")

print(f"{phone1.name} co gia la {phone1.price}")