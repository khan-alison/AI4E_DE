def sumtree(L): # Breadth-first, explicit queue
    tot = 0
    items = list(L) # Start with copy of top level
    while items:
        front = items.pop(0) # Fetch/delete front item
        if not isinstance(front, list):
            tot += front # Add numbers directly
        else:
            items.extend(front) # <== Append all in nested list
    return tot
L = [1, [2, [3, 4], 5], 6, [7, 8]]
# total = 0
# items = [1, [2, [3, 4], 5], 6, [7, 8]]
# round 1: pop phần tử 1 ra thì items còn [[2, [3, 4], 5], 6, [7, 8]]
#   => front = 1
#   => total = 0 + 1 =1
#   => items = ?
# round 2: pop phần tử [2, [3, 4], 5] ra thì items còn [6,[7, 8]]
#   => front = [2, [3, 4], 5]
#   => total = ?
#   => items = ?
# round 3:


print(sumtree(L))


def sumtree(L): # Depth-first, explicit stack
    tot = 0
    items = list(L) # Start with copy of top level
    while items:
        front = items.pop(0) # Fetch/delete front item
        if not isinstance(front, list):
            tot += front # Add numbers directly
        else:
            items[:0] = front # <== Prepend all in nested list
    return tot
# round 1: ???
#   => front = ?
#   => total = ?
#   => items = ?
# round 2:

