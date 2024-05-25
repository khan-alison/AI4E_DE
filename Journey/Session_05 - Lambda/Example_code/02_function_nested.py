def parent_func(x):
    def child_01(y):
        def child_02(z):
            print('x,y,z = {x},{y},{z}'.format(x = x, y = y, z = z))
        return child_02
    return child_01

print(parent_func('a')('b')('c'))