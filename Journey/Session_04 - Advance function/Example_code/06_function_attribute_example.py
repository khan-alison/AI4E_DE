SW_DELTA = 0
SW_MARK  = 1
SW_BASE  = 2

def stopwatch(): # đc coi là 1 object => nó sẽ có những attribute như vậy
   import time
   def _sw( action = SW_DELTA ):
      if action == SW_DELTA:
         return time.time() - _sw._time
      elif action == SW_MARK:
         _sw._time = time.time()
         return _sw._time
      elif action == SW_BASE:
         return _sw._time
      else:
         raise NotImplementedError
   _sw._time = time.time() # time of creation X
   return _sw

# test code
sw = stopwatch()
sw2 = stopwatch()
import time
time.sleep(1)
sw3 = stopwatch()
print(sw)
print(sw()) # defaults to "SW_DELTA"
sw(SW_MARK)
time.sleep(2)
print(sw())
print(sw2())
print(sw3())