def combine_all_args(a, *one, **two):
    print('a = {a}, one = {one}, two = {two}'.format(a = a, one = one, two = two))

t = (1, 2, 3)
d = dict()
d['1'] = 'a'
d['2'] = 'b'

combine_all_args('something', ((1, 2, 3, 4), {'1': 'a', '2': 'b'}) )

combine_all_args(1, 't', 'c', 5 , b = 1, c = 2)