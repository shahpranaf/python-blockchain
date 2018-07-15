name = "Pranav"
age = 29

def print_data() :
    print("My name is: " + name + " age is: " + str(age))


def print_data_arg(name, age) :
    print("My name is: " + name + "-" + str(age))

def decades_calc(time) :
    #return time//10
    return int(int(age)/10)

print_data()
print_data_arg("abc", 20)
print(decades_calc(32.32))