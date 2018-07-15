#1) Write a short Python script which queries the user for input (infinite loop with exit possibility) and writes the input to a file.

#2) Add another option to your user interface: The user should be able to output the data stored in the file in the terminal.

#3) Store user input in a list (instead of directly adding it to the file) and write that list to the file – both with pickle and json.

#4) Adjust the logic to load the file content to work with pickled/ json data.

import json
import pickle

def get_user_input(message):
    return input(message)


def user_interface():
    waiting_for_input = True
    u_data = []
    while waiting_for_input: 
        print("1: Input some data")
        print("2: Output the data")
        print("3: Output the JSON")
        print("4: Output the binary")
        print("q: Quit ")

        user_choice = get_user_input("Your choice: ")

        if user_choice == '1':
            data = get_user_input("Your input: ")
            u_data.append(data)
            with open('user.txt', mode='w') as f:
                f.write(data)
                f.write('\n')

            with open('user.json', mode='w') as f:
                
                f.write(json.dumps(u_data))

            with open('user.b', mode='wb') as f:
                f.write(pickle.dumps(u_data))

        elif user_choice == '2':
            with open('user.txt', mode='r') as f:
                content = f.readlines()
                for line in content:
                    print(line[:-1])

        elif user_choice == '3':
            with open('user.json', mode='r') as f:
                content = f.readlines()
                print(json.loads(content[0]))
        
        elif user_choice == '4':
            with open('user.b', mode='rb') as f:
                content = f.readlines()
                print(pickle.loads(content[0]))

        elif user_choice == 'q':
            waiting_for_input = False
            
            
user_interface()