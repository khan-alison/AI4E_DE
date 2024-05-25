def foo():
    x = 20

    def bar():
        global x
        x = 25
        print(f'inside bar x = {x}')
    
    print("Before calling bar: ", x)
    print("Calling bar now")
    bar()
    print("After calling bar: ", x)

foo()
print("x in main: ", x)