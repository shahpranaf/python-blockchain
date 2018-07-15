

# 1) Create a list of “person” dictionaries with a name, age and list of hobbies for each person. Fill in any data you want.
persons = [
    {
        'name': 'Panna',
        'age': 30,
        'hobbies': ['swimming', 'singing']
    },
    {
        'name': 'Rax',
        'age': 20,
        'hobbies': ['swimming', 'singing']
    }
]

print("===================")

# 2) Use a list comprehension to convert this list of persons into a list of names (of the persons).

person_names = [ el['name'] for el in persons ]
print(person_names)
print("===================")

# 3) Use a list comprehension to check whether all persons are older than 20.
person_names = [ el['age'] > 20 for el in persons ]
print(all(person_names))
print("===================")

# 4) Copy the person list such that you can safely edit the name of the first person (without changing the original list).
p2 = [el.copy() for el in persons]

p2[0]['name'] = 'dd'
print(p2)

print(persons)
print("===================")

# 5) Unpack the persons of the original list into different variables and output these variables.

a,b = persons
print(a)
print(b)