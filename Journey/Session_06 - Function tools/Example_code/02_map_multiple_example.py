l1 = [1, 2, 3, 4]
l2 = [4, 3, 2, 1]
t1 = (9, 8, 7, 6)
s1 = {0, 3}

transform = (lambda x, y: x + y)

# print(list(map(transform, l1, l2)))
# print(list(map(transform, l1, t1)))
print(list(map(transform, l1, s1)))