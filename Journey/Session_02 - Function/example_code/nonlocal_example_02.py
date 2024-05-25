def geek_func():
 
    # local variable to geek_func
    geek_name = "Day la level 1"
 
    # First Inner function
    def geek_func1():
        geek_name = "Day la level 2"
 
        # Second Inner function
        def geek_func2():
 
             # Declaring nonlocal variable
            nonlocal geek_name
            geek_name = 'Day la level 3'
 
            # Printing our nonlocal variable
            print(geek_name)
 
       # Calling Second inner function
        geek_func2()
 
        # Calling First inner function
    geek_func1()
 
    # Printing local variable to geek_func
    print(geek_name)
 
geek_func()