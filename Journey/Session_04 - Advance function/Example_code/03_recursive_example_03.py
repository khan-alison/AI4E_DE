def sumtree(L):
    tot = 0
    for x in L: # For each item at this level
        if not isinstance(x, list):
            tot += x # Add numbers directly 
        else:
            tot += sumtree(x) # Recur for sublists
    return tot
L = [1, [2, [3, 4], 5], 6, [7, 8]] # Arbitrary nesting
# tổng L = sumtree(1, sumtree(2, sumtree(3, 4), 5)6, sumtree(7,8))
# tổng của những phần tử không phải là list
# Đặt L = [1, A, 6, B]
# Trong đó: A = [2, [3, 4], 5]
    # A = [2, C, 5]
#           B = [7, 8]

# pesudo code:
# total = 0
# for x in L:
#   if x không phải là list:
#       tổng = tổng + x
#   else (nếu X là một list):
#       tổng = tổng + (Tổng của list con)

# check trái qua phải: 
# [1, 2, 3, 4, 5, 6, 7, 8]

print(sumtree(L)) # Prints 36
# Pathological cases
# print(sumtree([1, [2, [3, [4, [5]]]]])) # Prints 15 (right-heavy)
# print(sumtree([[[[[1], 2], 3], 4], 5])) # Prints 15 (left-heavy)