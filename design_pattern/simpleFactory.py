class Burger():
    """由于只提供了抽象方法，我们把它们叫抽象类"""
    name = ""
    price = 0.0
    type = "Burger"

    def getPrice(self):
        return self.price

    def setPrice(self, price):
        self.price = price

    def getName(self):
        return self.name

    def getType(self):
        return self.type


class cheeseBurger(Burger):
    """而cheese burger等6个由抽象类衍生出的子类，叫作具体类"""

    def __init__(self):
        self.name = "cheese burger"
        self.price = 10.0


class spicyChickenBurger(Burger):
    def __init__(self):
        self.name = "spicy chicken burger"
        self.price = 15.0


class Snack():
    name = ""
    price = 0.0
    type = "SNACK"

    def getPrice(self):
        return self.price

    def setPrice(self, price):
        self.price = price

    def getName(self):
        return self.name


class chips(Snack):
    def __init__(self):
        self.name = "chips"
        self.price = 6.0


class chickenWings(Snack):
    def __init__(self):
        self.name = "chicken wings"
        self.price = 12.0


class Beverage():
    name = ""
    price = 0.0
    type = "BEVERAGE"

    def getPrice(self):
        return self.price

    def setPrice(self, price):
        self.price = price

    def getName(self):
        return self.name


class coke(Beverage):
    def __init__(self):
        self.name = "coke"
        self.price = 4.0


class milk(Beverage):
    def __init__(self):
        self.name = "milk"
        self.price = 5.0


class simpleFoodFactory():
    @classmethod
    def createFood(cls, foodClass):
        foodIns = foodClass()
        print("Simple {} factory produce a instance.".format(foodIns.type))
        return foodIns


if __name__ == "__main__":
    # 简单工厂模式
    spicy_chicken_burger = simpleFoodFactory.createFood(spicyChickenBurger)
    print(spicy_chicken_burger.name, spicy_chicken_burger.price)
    chicken_wings_snack = simpleFoodFactory.createFood(chickenWings)
    print(chicken_wings_snack.name, chicken_wings_snack.price)
    coke_drink = simpleFoodFactory.createFood(coke)
    print(coke_drink.getName(), coke_drink.getPrice())

    milk_drink = milk()
    print(milk_drink.name, milk_drink.price)
