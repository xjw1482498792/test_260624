#锁
#创建一个 线程 协程 进程
#线程池 进程池

#创建线程
# import threading

# def task(number: int):
#     print(f'task---{number}')

# thread1 = threading.Thread(target=task,args=(1,))
# thread1.run()

#创建协程
# import asyncio
# async def task_async(number: int):
#     await asyncio.sleep(1)
#     print(f'task_async--{number}')

# async def main():
#     await asyncio.gather(task_async(2), task_async(1))    

# asyncio.run(task_async(1))
# asyncio.run(main())

# #创建进程
# import multiprocessing
# def task(number: int):
#     print(f'task---{number}')
# process1 = multiprocessing.Process(target=task, args=(3,))
# process1.run()


#创建线程池
# from concurrent.futures import ThreadPoolExecutor
# import time
# def task(number: int):
#     time.sleep(1)
#     return (f'task----{number}')

# with ThreadPoolExecutor(2) as p:
#     futures = [
#         p.submit(task, 1),
#         p.submit(task, 2),
#         p.submit(task, 3)
#     ]

#     for future in futures:
#         print(future.result())

# pool = ThreadPoolExecutor(max_workers=2)

# futures = [
#     pool.submit(task, 1),
#     pool.submit(task, 2),
#     pool.submit(task, 3),
# ]

# for future in futures:
#     print(future.result())

# pool.shutdown(wait=True)


#创建进程池
# from concurrent.futures import ProcessPoolExecutor

# def task(number):
#     return f'task---{number}'

# if __name__ == "__main__":
        
#     with ProcessPoolExecutor(2) as p:
#         futures = [
#             p.submit(task, 1),
#             p.submit(task, 2),
#             p.submit(task, 3)
#         ]

#         for future in futures:
#             print(future.result())    

