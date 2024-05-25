def gen():
    for i in range(10):
        yield i

a = gen()
print(next(a))
print(next(a))
print(next(a))
print(next(a))
print(next(a))

print()