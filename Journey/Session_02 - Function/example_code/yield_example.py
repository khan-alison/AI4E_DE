# nó sẽ return ra các thằng c1 được coi như phần tử của một list
def getFibonnaciSeries(num):
    c1, c2 = 0, 1
    count = 0
    while count < num:
        yield c1
        c3 = c1 + c2
        c1 = c2
        c2 = c3
        count += 1

fin = getFibonnaciSeries(7)
l = set(fin)
print(fin)
print(type(fin))
for i in fin:
    print(i)
for i in l:
    print(i)

print(list(fin))
print(l)