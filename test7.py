# from time import sleep, time
# from concurrent import futures

# start_time = time()

# def download_img(url):
#     sleep(1)
#     return f'{url} download complete'

# with futures.ThreadPoolExecutor(2) as executor:
#     results = executor.map(download_img, [f'url_{i}' for i in range(10)])

# for result in results:
#         print(result)

# end_time = time()

# print(f'Elapsed time: {end_time - start_time:.2f}')


# def get_value(key:str)->str:
#     match key:
#         case "key1":
#             return "value1"
#         case "key2":
#             return "value2"
#         case _:
#             return "default"
# for key in ['key1','key2','key3']:
#     print(get_value(key))        


# class MyNumbers:
#   def __iter__(self):
#     self.a = 1
#     return self
 
#   def __next__(self):
#     x = self.a
#     self.a += 1
#     return x
 
# myclass = MyNumbers()
# myiter = iter(myclass)

# print(next(myiter))
# print(next(myiter))
# print(next(myiter))
# print(next(myiter))
# print(next(myiter))

# class Solution:
#     def fib(self, n: int) -> int:
#         if n == 0:
#             return 0
#         elif n == 1:
#             return 1
#         else:
#             return self.fib(n - 1) + self.fib(n - 2)


# def my_decorator(func):
#     def wrapper():
#         print("函数执行前")
#         func()
#         print("函数执行后")
#     return wrapper

# @my_decorator
# def say_hello():
#     print("Hello!")

# say_hello()


# def all_process(execute):
#     def wrapper():
#         print("打开数据库")
#         execute()
#         print("关闭数据库")
#     return wrapper

# @all_process
# def execute():
#     print("执行数据库操作")

# execute()

# original_string = "Hello, World!"
# reversed_string = original_string[::-1]
# print(reversed_string)

# class cat:
#     def __init__(self, name):
#         self.name = name

#     def meow(self):
#         print(f"{self.name} says: Meow!")

#     def fun1():
#         print("hello")    

# cat.fun1()
# my_cat = cat("Fluffy")
# my_cat.meow()

# import threading
# from concurrent.futures import ThreadPoolExecutor
# from time import sleep
# import random

# counter = 0
# lock = threading.Lock()

# def task():
#     global counter
#     temp = counter
#     # with lock:        # ← 不加这个，counter 会被多线程同时改，结果乱掉
#     # sleep(random.uniform(0.1, 0.5))
#     # sleep(0.0000000000000000000000000000000000000000000000000000001)
#     counter = temp + 1

# with ThreadPoolExecutor(max_workers=10) as pool:
#     for _ in range(10):
#          pool.submit(task)

# print(counter)  # 加锁 → 100，不加锁 → 可能是 97、98 等随机值


def my_function(*args, **kwargs):
    print("args:", args)
    print("kwargs:", kwargs)

my_function(1, 2, 3, name="John", age=25)

