def mysum(L):
    if not L: return 0
    return nonempty(L)

def nonempty(L):
    return L[0] + mysum(L[1:])

print(mysum([1, 2, 3, 4, 5]))
#print(nonempty([1, 2, 3, 4, 5]))