#闭包
# def fun1(num1):
#     def fun2():
#         nonlocal num1
#         num1 += 1
#         return num1
#     return fun2

# my_fun = fun1(3)
# print(my_fun()) 
# print(my_fun()) 
# my_fun()

#装饰器
# def deco(my_fun):
#     def wrapper(*args, **kwargs):
#         print("begin")
#         res = my_fun(*args, **kwargs)
#         print("end")
#         return res + 1
#     return wrapper

# @deco
# def fun1(num):
#     return num

# print(fun1(3))

#迭代器和生成器

# list1 = list([1,2,3])
# iter1 = iter(list1)
# print(next(iter1))
# print(next(iter1))


# def fun1():
#     i = 0
#     while i < 5:
#         yield i
#         i += 1

# iter2 = fun1()
# print(next(iter2))
# print(next(iter2))

#拉姆达
# fun = lambda x, y : x + y

# iter1 = (tmp for tmp in [1,2,3])
# list1 = [tmp for tmp in [1,2,3]]

# print(list1)
# print(next(iter1))


#创建线程 协程 进程 线程池 进程池
import asyncio

def task():
    print("tasking---------")

#线程
# from threading import Thread
# thread1 = Thread(target=task)
# thread1.run()  

#进程
# from multiprocessing import Process
# p1 = Process(target=task)
# p1.run()

#协程
# async def task2():
#     await asyncio.sleep(1)
#     print("task2")

# async def main():
#     await asyncio.gather(task2(), task2())

# asyncio.run(main())

#线程池
# from concurrent.futures import ThreadPoolExecutor

# with ThreadPoolExecutor(2) as pool:
#     res = [pool.submit(task) for _ in range(3)]
#     for _ in res:
#         pass

#进程池
# from concurrent.futures import ProcessPoolExecutor  

# if __name__ == '__main__':
#     with ProcessPoolExecutor(2) as pool:
#         res = [pool.submit(task) for _ in range(3)]
#         for _ in res:
#             pass