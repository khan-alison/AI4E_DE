
l1 = [1, 2, 3, 4, 5]
l2 = [5, 4, 3, 2, 1]
s1 = {9, 8, 7, 6, 5, 4}

# [f(x) for x in iterable if condition]
a = [(lambda x, y: x + y)(x, y) for x in l1 for y in l2]

a1 = {(x - y): (lambda x, y: x + y)(x, y) for x in l1 for y in l2}

# print(a1)
# # Advance - multiple
# b = [(lambda x, y: x + y)(x, y) for x, y in zip(l1, l2)]
# print(b)

c = [(lambda x, y, z: x + y + z)(x, y, z) for x, y, z in zip(l1, l2, s1)]
print(c)

d = {(x + y + z): (lambda x, y, z: x + y + z)(x, y, z) for x, y, z in zip(l1, l2, s1)}
print(d)