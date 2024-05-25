l = [(lambda x: x + 1)(x) for x in range(5)]
# đây là 1 transform để tạo ra 1 iterator
# trong quá trình tạo iter, mỗi 1 loop sẽ có 1 local x
# local x này sẽ biến mất sau khi kết thúc loop
# => sau khi kết thúc comprehension => x cũng kết thúc

print('a')