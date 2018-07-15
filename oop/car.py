from vehicle import Vehicle

class Car(Vehicle):
    # top_speed = 100
    # warning = []

    def __init__(self):
        super().__init__()

   
car1 = Car()
car1.top_speed = 200
car1.set_warnings("Hello Brother")
car1.drive()
print(car1.get_warnings())
print(car1)
