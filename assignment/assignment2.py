names = ['ab', 'cde', 'johNy', 'jamny'];

for name in range(len(names)):
    if len(names[name]) >= 5:
        print((names[name]))
        if names[name].find('n') != -1 or names[name].find('N') :
            print("Includes N or n")

while len(names):
    print(names)
    names.pop()
    


