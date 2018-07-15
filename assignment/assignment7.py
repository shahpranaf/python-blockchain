#1) Create a Food class with a “name” and a “kind” attribute as well as a “describe() ” method (which prints “name” and “kind” in a sentence).

class Food():

    name = "Sandwich"
    kind = "Snacks"

    def __init__(self):
        self.name = "Burger"
        self.kind = "Fastfood"

    def __repr__(self) :
        temp = {
            "name": self.name,
            "kind": self.kind
        }
        return temp
    

    def describe(self):
        print("I love {} which is of kind {}".format(self.name, self.kind))

    
    @classmethod
    def describeClassMethod(cls):
        print("I love {} which is of kind {}".format(cls.name, cls.kind))

    
    @staticmethod
    def describeStatic(name, kind):
        print("I love {} which is of kind {}".format(name, kind))


food = Food()
food.describe()
food.describeClassMethod()
Food.describeStatic('Beans', "Pulses")

#2) Try turning describe()  from an instance method into a class and a static method. Change it back to an instance method thereafter.

#3) Create a  “Meat” and a “Fruit” class – both should inherit from “Food”. Add a “cook() ” method to “Meat” and “clean() ” to “Fruit”.

class Meat(Food):

    def cook(self):
        print("this is cook {}".format(self.name))

#4) Overwrite a “dunder” method to be able to print your “Food” class.
class Fruit(Food):

    def __init__(self):
        super().__init__()


    def clean(self):
        print(self.__dict__)



meat = Meat()
meat.cook()

fruit = Fruit()
fruit.clean()
