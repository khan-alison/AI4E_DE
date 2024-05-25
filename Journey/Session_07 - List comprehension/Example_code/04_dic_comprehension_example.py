

iter = [1, 2, 3, 4, 5, 5]

a = { x: (lambda x: x + 1)(x) for x in iter if True}

print (a)