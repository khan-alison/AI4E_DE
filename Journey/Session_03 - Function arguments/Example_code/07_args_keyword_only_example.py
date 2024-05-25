def do_something(a, *b, c, **d):
    print('a = {a}, b = {b}, c = {c}, d = {d}'.format(a = a, b = b, c = c, d = d))

def do_something_else(*, a, b, c):
    print('a = {a}, b = {b}, c = {c}'.format(a = a, b = b, c = c))

# code example
do_something(1, ('a', 'b', 3), 4, c = 5, d = {'a': 1})

# code example here
do_something_else(b = 1, a = 2, c = 3)