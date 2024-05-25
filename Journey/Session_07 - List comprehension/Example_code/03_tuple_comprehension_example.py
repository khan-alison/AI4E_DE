# this is special, why?
iter = (1, 2, 3, 4, 5, 5, 5)

gen = ((lambda x: x + 1)(x) for x in iter if x % 2 == 1)

a = set(gen)

print(a)