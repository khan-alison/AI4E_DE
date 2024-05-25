#CONVENTION

#INDENTATION

#aligned with opening delimiter:
from re import X


foo = long_function_name(var_one, var_two
                        var_three, var_four)

#add 4 spaces (an extra level of indentation) to distinguish arguments from the rest:
def long_function_name(
        var_one, var_two, var_three,
        var_four):
    print(var_one)

#hanging indents should add a level:
foo = long_function_name(
    var_one, var_two,
    var_three, var_four)

# with if-statement, if conditional part is too long and need to break into multiple lines:
#no extra indentation:
if (condition_one and
    condition_two):
    do_something()

#add a comment to provide some distinction in editors and support syntax highlighting:
if (condition_one and
    condition_two):
    #since both condition are true, we can frobnicate
    do_something()

#add extra indentation on the conditional continuation line
if (condition_one and 
        condition_two):
    do_something()

#Tabs or spaces: Spaces are preferable method for indentation, while tabs are only used to maintain consistence with code that is already indented with tabs.
#Python does not allow mixing tabs and spaces for indentation

#MAXIMUM LENGTH
#Limit all lines to a maximum of 79 characters

#Should a line break before or after a binary operation?
income = (gross_wages
          + taxable_interest
          + (dividends - qualified_dividends)
          - ira_deduction
          - student_loan_interest)


#Blank line
#Surround top-level function and class definition with 2 blank lines
#method definitions inside a class are surrounded by a blank line
#blank line can also be used to seperate groups of related functions or to indicate logical sections

#whitespace in Expresion and Statement
#avoid extraneous whitespace in the following cases:

#immediately inside brakets, parenthesis or braces:
spam = ( ham[ 1 ], { egg: 2 } ) ===> spam = (ham[1], {egg: 2})

#between trailing command and a following close parenthesis:
foo = (0, ) ===> foo = (0,)

#immediately before comma, semicolon or colon:
#however in a slice a colon acts like a binary operator, and should have equals of space on either side
if x == 4 : print(x , y) ; x , y = y , x ====> if x == 4: print(x, y); x, y = y, x 
ham[1: 9], hame[1, 9] ===> ham[1,9]

#immediate before the open parenthesis that start the arguement list of a function call:
spam (1) ===> spam(1)

#Immediately before the open parenthesis that starts an indexing or slicing:
dct ['key' ====> dct['key']

#OTHER RECOMMENDATION
#avoid trailing whitespace as it is invisible and can be confusing
#always surround binary operator with whitespace on either side: =, ==, <=, >=, etc
# if operators have different priorities, consider using whitespace with operators that have lower priorities:
i=i+1 ====> i = i + 1
x = x * 2 + 1 ===> x = x*2 + 1
#compound statement are usually discouraged:
if foo = 'blah': do_thing_one()
do_thing_two(); do_thing_three()
====>
if foo = 'blah':
    do_thing_one()
do_thing_two()
do_thing_three()

#COMMENT
#comment should be a complete sentences, the first word should be capitalized
#BLOCK COMMENT: block comments apply to all code following them, and are intended to the same level as that code. Block commnet starts with # and a space
#INLINE COMMNET: inline comment is a comment that is in the same as that code and should be separated from that code with at least 2 spaces. They start wuth # and a space


#NAMING CONVENTION

#Descriptive: Naming styles
#lower case, lower case with underscore, UPPER CASE, UPPER CASE WITH UNDERSCORE, capitalized words, mixed case, etc

#Presciptive: Naming convention
#Package and Module name: Modules should have short, all-lowercase names. Underscore can be used if it provides readability.
#class name:



