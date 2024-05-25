def run(a):
    pass

def laubang(*, a):
    pass

def fun(*a, **b):
    pass

[lambda x: x + 1 for x in range(4)]

# object class
class Bicyle:
    
    def __init__(self, speed, color) -> None:
        self.speed = speed
        self.color = color
        
    def run(self):
        return self.speed + 1
    
    def laubang(self):
        return self.speed ** 2
    
    def add(datatype, *args):
        if datatype =='int':
            answer = 0
            
        if datatype =='str':
            answer =''
            
        for x in args:
            answer = answer + x
    
        print(answer)
    
class SportBicycle(Bicyle):
    
    def __init__(self, speed, color, wheel) -> None:
        super().__init__(speed, color)
        self.wheel = wheel
        
    def run(self):
        return self.speed + 2
    
    def add(self):
        pass

A = Bicyle(1,2)
B = SportBicycle(1,2,3)

print(A.run())
print(B.run())
