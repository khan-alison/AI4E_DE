def function(a, b, c, d, e):
    print('a = {a}, b = {b}, c = {c}, d = {d}, e = {e}'.format(a = a, b = b, c = c, d = d, e = e))


args = (1, 2)
args = args + (3,)

dic_args = {'d' : 4, 'e': 5}

a = function(*args, **dic_args)