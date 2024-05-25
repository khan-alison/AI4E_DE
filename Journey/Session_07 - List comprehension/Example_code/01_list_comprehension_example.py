iter = (1, 2, 3, 4, 5, 5, 5)

a = [(lambda x: x + 1)(x) for x in iter if x % 2 == 1]

print (a)