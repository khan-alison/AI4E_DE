l1 = [1, 2, 3, 4, 5]

lam = (lambda x: x % 2 == 1)
lam_2 = lambda x: x + 1

print(list(filter(lam, l1)))

