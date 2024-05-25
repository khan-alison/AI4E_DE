
def func(a: float = 5) -> int:
    if (not isinstance(a, str)):
        return 'error'
    return 'okay'

print(func.__annotations__)

print(func('s'))