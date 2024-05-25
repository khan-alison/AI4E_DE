check = 0
count = 0

def func_1():
    ''''''
    global check
    global count
    # check đã từng chạy qua hàm 3 hay chưa, nếu rồi thì do something
    if check != 3:
        count = count + 1
    if count == 5:
        check = 3
    print('check: ' + str(check) + ' count: ' + str(count))

def func_3():
    global check
    if check == 3:
        print('meet expect')
        check = 'quit'

while(True):
    ''''''
    func_1()
    func_3()
    if check == 'quit':
        break# Calling First inner function
    geek_func1()
 
    # Printing local variable to geek_func
    print(geek_name)
 
geek_func()