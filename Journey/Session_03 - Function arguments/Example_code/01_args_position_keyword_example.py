def function(a, b, c):
    print('a = {a}, b = {b}, c = {c}'.format(a = a, b = b, c = c))

def function_02(a, b, c, d, e):
    print('a = {a}, b = {b}, c = {c}, d = {d}, e = {e}'.format(a = a, b = b, c = c, d = d, e = e))

function(1, 2, 3)
function(c = 1, a = 2, b = 3)

# position -> keyword

function(1, 2, c = 4)
function_02(9, 9, 1, e = 4, d = 3)