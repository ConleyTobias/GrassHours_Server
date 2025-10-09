from datetime import datetime
import time
import bcrypt

def log(func):
    def wrapper():
        start = time.perf_counter()
        func()
        print(f"{func.__name__}() ran @{datetime.now()}, taking {time.perf_counter() - start} seconds)")
    return wrapper

def timeout_expired(seconds):
    def decorator(function):
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = function(*args, **kwargs)
            if time.perf_counter() - start > seconds:
                raise Exception(f"TimeoutExpired: Over {seconds} seconds")
            return result
        return wrapper
    return decorator