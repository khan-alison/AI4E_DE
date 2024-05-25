
def geek_func():
     
    # local variable to geek_func
    geek_name = "geek"
    # Inner function
 
    def geek_func2():
       
        # Declaring nonlocal variable
        nonlocal geek_name #naming ref
        geek_name = 'GeekForGeeks'
         
        # Printing our variable
        print(geek_name)
         
    # Calling inner function
    geek_func2()
     
    # Printing local variable
    print(geek_name)
 
geek_func()