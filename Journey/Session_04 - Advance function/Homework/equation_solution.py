import math
import numpy as np

def quadratic_equation(a,b,c):
    if a == 0:
        print('This is not a quadratic equation')
    else:
        delta = b*b - 4*a*c
        if delta < 0:
            print('The equation has no root')
        elif delta == 0:
            x = -b/(2*a)
            print('The equation has equal root: {0}'.format(x))
        else:
            x1 = (-b + math.sqrt(delta) ) / (2*a)
            x2 = (-b - math.sqrt(delta) ) / (2*a)
            print('The equation has 2 roots: {0} and {0}'.format(x1,x2))

quadratic_equation(1,-3,1)

def cubic_equation(a,b,c,d):
    if a == 0:
        print('This is not a cubic equation')
    else:
        delta = b*b - 3*a*c
        abs_delta = abs(delta)
        k = (9*a*b*c - 2*b*b*b - 27*a*a*d) / (2 * math.sqrt(abs_delta * abs_delta * abs_delta))
        if delta < 0:
            x = (math.sqrt(abs_delta)/3 * a) *  ( np.cbrt(k + math.sqrt(k*k + 1)) +  np.cbrt(k - math.sqrt(k*k + 1))) - b / 3*a
            print('This equation has 1 root: {}'.format(x))
        if delta == 0:
            x = (-b + np.cbrt(b*b*b - 27*a*a*d)) / 3*a
            print('This equation has 1 root: {}'.format(x))
        if delta > 0: 
            if abs(k) <= 1:
                x1 = (2 * math.sqrt(delta) * np.cos(np.arccos(k/3)) - b) / 3*a
                x2 = (2 * math.sqrt(delta) * np.cos(np.arccos(k/3) - 2 * 3.14 / 3) - b) / 3*a
                x3 = (2 * math.sqrt(delta) * np.cos(np.arccos(k/3) + 2 * 3.14 / 3) - b) / 3*a
                print('This equation has 3 roots: {}, {}, {}'.format(x1, x2, x3))
            else: 
                x = (-b + np.sqrt(b*b*b - 27*a*a*d)) / 3*a
                print('This equation has 1 root: {}'.format(x))

cubic_equation(1,2,-4,1)


def blank_to_underscore1(string_input, string_output, i):
    if len(string_input) == len(string_output):
        return string_output
    else:
        if string_input[i] == ' ':
            string_output = string_output + '_'
        else:
            string_output = string_output + string_input[i]
            i = i + 1
        return blank_to_underscore1(string_input, string_output, i)
