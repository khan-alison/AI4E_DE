import random

#total_nums = 0 #the total of generated list of numbers
#multiply_nums = 0 #the total of multiplication
count_func_1 = 0 
count_func_2 = 0
count_multiply_2 = 0
count = 0 #the numbers of loops
reset_nums = 0 #the number of reset times
total_count = 0 #the total of count_func_1 and count_func_2

def generator_nums():
    lst_nums = []
    for i in range(5):
        lst_nums.append(random.randint(1,100))
    return lst_nums
    
def total_of_nums(lst):
    total_nums = 0
    global count_func_1
    global count_func_2
    global reset_nums
    for i in range(0, len(lst)):
        total_nums = total_nums + lst[i]
    if total_nums % 3 == 0:
        count_func_1 = count_func_1 + 1
    elif total_nums % 5 == 0:
        count_func_2 = 0
        reset_nums = reset_nums + 1  

def multiplication_nums(lst):
    multiply_nums = 0
    global count_func_2
    global count_multiply_2
    for i in range(0, len(lst)):
        multiply_nums = multiply_nums * lst[i] 
    if multiply_nums % 5 == 0:
        count_func_2 = count_func_2 + 1
        count_multiply_2 = count_multiply_2 + 1

while(True): # dieu kienj while(true) nghia la gi?
    count = count + 1
    a = generator_nums()   
    total_of_nums(a) 
    multiplication_nums(a)
    total_count = count_func_1 + count_func_2
    if ((total_count > 10) and (count_func_2 > 1)):
        print(a)
        print(total_count)
        print(count_func_2) 
        print('The number of loops is', count)
        print('The number of times total number is divisible by 3 is', count_func_1)
        print('The number of times multiplication number is divisible by 5 is', count_multiply_2)
        print('The number of reset time is', reset_nums)
        break