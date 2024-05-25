
# Function to take multiple arguments
from typing import overload


def add(datatype, *args):
    if datatype =='int':
        answer = 0
           
    if datatype =='str':
        answer =''
    for x in args:
        answer = answer + x
   
    print(answer)
   
# Integer
# add('int', 5, 6)
   
# # String
# add('str', 'Hi ', 'Geeks', )

class ModelFactory:
    
    def __init__(self, name) -> None:
        self.name = name
    
    def minus(a, b):
        from pandas import minus
        return minus(a,b)

    def sum(a, b, c):
        from numpy import array
        return array(a,b,c)

class FactoryTwo(ModelFactory):
    def __init__(self, name) -> None:
        super().__init__(name)
    
    def add(a, b):
        import sys
        return sys(a,b)

model_01 = ModelFactory('model1')
model_01.minus()

model_02 = FactoryTwo('model2')
model_02