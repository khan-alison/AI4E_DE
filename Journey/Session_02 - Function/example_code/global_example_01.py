c = 0

def add():
    global c
    c = c + 2 # increment by 2
    print("Inside add():", c)

add()

def func():
    local_variable = 'local'
    print(local_variable)
    
local_variable = 'out of local'
print(local_variable)