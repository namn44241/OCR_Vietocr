import time

def timer(func):
    def wrapper(*args, **kwargs):
        t0 = time.time()
        result = func(*args, **kwargs)
        t1 = time.time()
        print(f"{func.__name__} chạy trong {t1 - t0} s")
        return result
    
    return wrapper
    