a = lambda x: lambda y: lambda z: \
    print('x,y,z = {x},{y},{z}'.format(x = x, y = y, z = z))

print(a('a')('b'))