class Vehicle:
    
    def __init__(self, top_speed = 100):
        self.top_speed = top_speed
        self.__warning = []


    def __repr__(self) :
        return "Hello panna"    


    def set_warnings(self, warning_text):
        self.__warning.append(warning_text)

    def get_warnings(self):
        return self.__warning


    def drive(self):
        print("{} Top speed of this car is {}".format(self.__warning, self.top_speed))

# car1 = Car()
# car1.top_speed = 200
# car1.set_warnings("Hello Brother")
# print(car1.get_warnings())
