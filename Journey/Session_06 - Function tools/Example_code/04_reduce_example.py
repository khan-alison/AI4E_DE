from functools import reduce
from msilib.schema import Error

lambda_01 = lambda x, y: x + y 

# print(reduce(lambda_01, [1, 2, 3, 4]))

# lambda_01(lambda_01(lambda_01(1, 2), 3),4)

l1 = [['a', 1], [2, 2], ['a', 3]]
lambda_03 = lambda x: x[0] == 'a'
l2_afterfilter = list(filter(lambda_03, l1))
# print(l2_afterfilter)

lambda_02 = lambda x, y: [str(x[0]) + str(y[0]), x[1] + y[1]]

# print(reduce(lambda_02, l2_afterfilter))

# em có 1 tr rows dữ liệu
# đầu tiên: dùng map để chuẩn hóa dữ liệu
# dùng filter để lấy ra sample cần sử dụng cho bài toán
# dùng reduce để tính kết quả cuối cùng


l4 = [1, 2, 3, '4', 'a', 'b', 7, 8]

def check(x):
    if type(x) == int:
        return x
    else:
        try:
            a = int(x)
            return a
        except:
            return None # return null

l5 = list(filter(lambda x: type(x) == int, map(check, l4)))

print(l5)