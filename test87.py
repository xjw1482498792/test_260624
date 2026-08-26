##常用python相关，主要考察真实性
##如常用内置模块，文件流操作
##线程协程相关等

#创建线程
# def task1():
#     print("task1 is running...")

# from threading import Thread

# t1 = Thread(target=task1)
# t1.run()

# #创建进程
# def task1():
#     print("task1 is running...")

# from multiprocessing import Process
# p1 = Process(target=task1)
# p1.run()

#创建协程asynchronous
# import asyncio
# async def task1(num):
#     await asyncio.sleep(1)
#     print(f"task{num} is running...")

# async def all_task():
#     await asyncio.gather(task1(1),task1(2),task1(3))

# asyncio.run(task1(0))    
# asyncio.run(all_task())   

#创建线程池
# import time
# from concurrent.futures import ThreadPoolExecutor

# def task1():
#     time.sleep(1)
#     print("task1 is running...")

# with ThreadPoolExecutor(3) as p:
#     futures = (p.submit(task1) for _ in range(3))
#     for future in futures:
#         pass

#创建进程池
# import time
# from concurrent.futures import ProcessPoolExecutor

# def task1():
#     time.sleep(1)
#     print("task1 is running...")

# if __name__ == "__main__":
#     with ProcessPoolExecutor(3) as p:
#         futures = (p.submit(task1) for _ in range(3))
#         for future in futures:
#             pass

#文件流及时间相关模块
from datetime import datetime 
import time
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
now_time = time.perf_counter()
print(f'now is {now}')
print(f'now time is {now_time}')

line = f'执行时间----->{now}\n'
url = "C:\\Users\\Administrator\\Downloads\\output.txt"
with open(url, "a", encoding="utf-8") as file:
# with open("output.txt", "a", encoding="utf-8") as file:
    file.writelines(line)

#字典结构