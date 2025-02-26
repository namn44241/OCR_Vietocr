import time
from math import *

def timer(func):
    def wrapper(*args, **kwargs):
        t0 = time.time()
        result = func(*args, **kwargs)
        t1 = time.time()
        print("{:.4f}:                {}".format(t1 - t0, func.__name__))
        return result
    
    return wrapper