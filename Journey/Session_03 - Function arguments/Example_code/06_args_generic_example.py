
def do_something(a, b, c, d, e):
    print('a = {a}, b = {b}, c = {c}, d = {d}, e = {e}'.format(a = a, b = b, c = c, d = d, e = e))

def wake_something(a,b,c,d,e,f,j,k):
    print('a = {a}, b = {b}, c = {c}, d = {d}, e = {e}, f = {f}, j = {j}, k = {k}'.format(a = a, b = b, c = c, d = d, e = e, f = f, j = j, k = k))

def generic_ex(func, *arg_tupl, **args_dict):
    print('Calling function name: {name}'.format(name = func.__name__))
    return func(*arg_tupl, **args_dict)

# data => dieu kien chay chuong trinh khac di => ham phai goi co the thay doi => tham so truyen vao co the thay doi

generic_ex(do_something, 1, 2, *(3, 4), **{'e': 5})
generic_ex(wake_something, 1, 2, *(3, 4, 5, 6), **{'j': 7, 'k': 8})
