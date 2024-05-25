def print_one(input): # => trong bộ nhớ sẽ tạo vùng nhớ để lưu object logic của hàm
    print(input)

a = ['something', 'here', 'will', 'be', 'printed']

def print_by_passing_func(func, a):
    if isinstance(a, list):
        for item in a:
            func(item)

print_by_passing_func.count = 0

print(dir(print_by_passing_func))

#print_by_passing_func.count = 0


#print_by_passing_func(print_one, a)
