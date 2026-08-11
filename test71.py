###线程 协程 进程， 线程池 进程池
###迭代器 生成器 装饰器

#协程
# import asyncio
# async def task(number):
#     await asyncio.sleep(1)
#     print(f'task----{number}')

# async def all_task(): 
#     await asyncio.gather(
#         task(1), 
#         task(2), 
#         task(3) 
#     )
# asyncio.run(all_task())
# asyncio.run(all_task())
# asyncio.run(task(1))

#线程
# import threading

# def task(number):
#     print(f'task----{number}')

# t1 = threading.Thread(target=task, args=(1,))
# t1.run()

# #进程
# import multiprocessing

# def task(number):
#     print(f'number---{number}')
# p1 = multiprocessing.Process(target=task, args=(2,))
# p1.run()

#线程池
# from concurrent.futures import ThreadPoolExecutor
# import time

# def task(number):
#     time.sleep(1)
#     return (f'task----{number}')

# with ThreadPoolExecutor(2) as p:
#     futures = [
#     p.submit(task, 1),
#     p.submit(task, 2),
#     p.submit(task, 3)
#     ]
#     for future in futures:
#         print(future.result())

#进程池
# from concurrent.futures import ProcessPoolExecutor

# def task(number):
#     return f'task---{number}'



# p = ProcessPoolExecutor(2)


# if __name__ == "__main__":
#     futures = [
#         p.submit(task,1),
#         p.submit(task,2),
#         p.submit(task,3)
#     ]
#     for future in futures:
#         print(future.result())

#     p.shutdown()    
# # if __name__ == "__main__":
# #     with ProcessPoolExecutor(2) as p:
# #         futures = [
# #             p.submit(task,1),
# #             p.submit(task,2),
# #             p.submit(task,3)
# #         ]
# #         for future in futures:
# #             print(future.result())


#迭代器
# list1 = [1,3,4,6]
# iter1 = iter(list1)
# print(next(iter1)) 
# print(next(iter1)) 

# class counter():
    
#     def __init__(self, init, limit):
#         self.init = init
#         self.limit = limit
#         self.cur  = None

#     def __iter__(self):
#         return self

#     def __next__(self):
#         self.cur = self.init
#         self.init += 1
#         if self.cur < self.limit:
#             return self.cur
#         else:
#             raise StopIteration

# c1 = counter(0,5)           
# iter2 = iter(c1)
# for tmp in iter2:
#     print(tmp)

# iter3 = iter(counter(0,3))    
# print(next(iter3))
# print(next(iter3))

# #生成器
# def gen(init, max):

#     while init < max:
#         yield init
#         init += 1

# gen1 = gen(0, 5)     
# print(next(gen1)   )
# print(next(gen1)   )

# for tmp in gen(0,3):
#     print(tmp)


# #装饰器

# def decorate1(num):
#     def decorate(ori):
#         def wrapper(*args, **kwargs):
#             print("before")
#             for _ in range(num):                
#                 print(ori(*args, **kwargs))
#             print("end")
#         return wrapper    
#     return decorate    

# @decorate1()
# def origin(name):
#     return f'my name is {name}'


# origin('xiaohua')


#单例函数

    