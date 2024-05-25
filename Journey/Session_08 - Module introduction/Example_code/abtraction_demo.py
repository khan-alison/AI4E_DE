
from abc import ABCMeta, abstractclassmethod, abstractmethod


class Vehicle(metaclass=ABCMeta):
    def __init__(self, color, time) -> None:
        self.color = color
        self.time = time
    
    def get_info(self):
        print(self.run())
    
    @abstractmethod
    def run(self) -> str:
        pass
    
class Bike(Vehicle):
    def __init__(self, color, time) -> None:
        super().__init__(color, time)
    
    def run(self):
        return 'xe dap'


class Motobike(Vehicle):
    
    def __init__(self, color, time) -> None:
        super().__init__(color, time)
        
    def run(self):
        # do something
        return 'xe may'
    

# v = Vehicle(2,3)
b = Bike(2,3)
b.get_info()
# m = Motobike(2,3)
# m.get_info()