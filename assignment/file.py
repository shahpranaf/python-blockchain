""" ============ Write ============= """
#f = open('demo.txt', mode='w')
#f.write("Hello pranav !!!")
#f.close()

""" ============ Read ============= """
#f = open('demo.txt', mode='r')
#f_content = f.read()
#f.close()

#print(f_content)


""" ============ Write Multiline ======== """
#f = open('demo.txt', mode='a')
#f.write("Hello pranav !!!\n")
#f.close()

""" ======= Read Multiline ========="""
#f = open('demo.txt', mode='r')

# ===== Read whole file at once ==== #

#f_content = f.read()
#print(f_content)


# ===== Get all lines of file in list ==== #

#f_content = f.readlines()

#for line in f_content:
#    print(line[:-1])


# ===== Get one line of file ==== #
    
#line = f.readline()
#while line:
 #   print(line)
  #  line = f.readline()
   

#f.close()

#print(f_content)


# ===== With file handling ==== #

with open('demo.txt', mode='r') as f:
    line = f.readline()
    while line:
        print(line)
        line = f.readline()   

print("Done")
