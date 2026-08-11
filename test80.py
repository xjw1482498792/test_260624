# import time
# from functools import wraps

# def timer(func):
#     # @wraps(func)
#     def wrapper(*args, **kwargs):
#         start = time.perf_counter()
#         try:
#             return func(*args, **kwargs)
#         finally:
#             elapsed = time.perf_counter() - start
#             print(f"{func.__name__} 耗时：{elapsed:.6f} 秒")

#     return wrapper


# @timer
# def task(delay):
#     time.sleep(delay)
#     return "完成"


# result = task(2)
# print(result)


#手写计时装饰器

import time

def my_deco(func):

    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        print(f'总耗时：{end - start}')
        print(time.strftime("%Y-%m-%d %H:%M:%S"))
    return wrapper    

@my_deco
def my_func(seconds):
    time.sleep(seconds)
    print("my_func-----------------")

my_func(2)    