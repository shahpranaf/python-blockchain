import functools
# 1) Write a normal function that accepts another function as an argument. Output the result of that other function in your “normal” function.
def normal(f_name, *args):
    #print(args)
    print( '{:^20}'.format(f_name(args)) )

def another(arg) :
    return "Hello"


normal(another)



#2) Call your “normal” function by passing a lambda function – which performs any operation of your choice – as an argument.


normal( lambda el: 5*5 )

#3) Tweak your normal function by allowing an infinite amount of arguments on which your lambda function will be executed.     

normal( lambda args: functools.reduce(lambda arg_sum, arg_amt: arg_sum+arg_amt, args, 0), 1,2,3 )

#4) Format the output of your “normal” function such that numbers look nice and are centered in a 20 character column.

def normal(f_name, *args):
    #print(args)
    print( '{:^20}'.format(f_name(args)) )