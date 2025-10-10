from datetime import datetime
import time
import json

def log(func):
    def wrapper():
        start = time.perf_counter()
        func()
        print(f"{func.__name__}() ran @{datetime.now()}, taking {time.perf_counter() - start} seconds)")
    return wrapper

def get_json(path):
    with open(path, 'r') as file:
        return json.load(file)

def dump_json(path, data):
    with open(path, 'w') as file:
        json.dump(data, file, indent=4)