def mysum(L):
    print(L)
    if not L:
        return 0
    else:
        return L[0] + mysum(L[1:])

print(mysum([1, 2, 3, 4, 5]))

def mysum(L):
    return 0 if not L else L[0] + mysum(L[1:]) # Use ternary expression


def mysum(L):
    return L[0] if len(L) == 1 else L[0] + mysum(L[1:]) # Any type, assume one
def mysum(L):
    first, *rest = L
    return first if not rest else first + mysum(rest) # Use 3.X ext seq assign


mysum((1,2,3,4,5))