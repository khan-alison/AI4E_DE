def one_star_function(*variables):
    print(variables, ' --- ', type(variables))

one_star_function(1, 2, 3)

one_star_function(1, 2, 3, 4, 5, 6)

def two_stars_function(**variables):
    print(variables, ' --- ', type(variables))

two_stars_function(a = 1, b = 2, c =3)
