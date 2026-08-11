# #异步
# import asyncio
# import time
# async def fun():
#         print("begin") 
#         await  asyncio.sleep(1)
#         print("end") 

# asyncio.run(fun())   


#手写线程池，进程池,线程，进程，协程
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def task(input):
    return(f'task-{input}')

#线程池
# with ThreadPoolExecutor(2) as pool:
#     f1 = pool.submit(task,"123")
#     res1 = f1.result()
#     print(res1)

#进程池 
# def main():
#     with ProcessPoolExecutor(2) as pool:
#         f1 = pool.submit(task,"123")
#         res1 = f1.result()
#         print(res1)   IO

# if __name__ == "__main__":
#     main()

#线程
# import threading

# t1 = threading.Thread(target=task, args=("123",))
# t1.start()

#进程
from multiprocessing import Process

if __name__ == "__main__":
    process = Process(
        target=task,
        args=("进程A",),
    )

    process.start()  # 启动子进程
    # res = process.join()
    # print(res)





#通信
# from multiprocessing import Process, Queue


# def producer(queue):
#     queue.put("hello")
#     queue.put({"amount": 100})


# def consumer(queue):
#     print(queue.get())
#     print(queue.get())


# if __name__ == "__main__":
#     queue = Queue()

#     process1 = Process(target=producer, args=(queue,))
#     process2 = Process(target=consumer, args=(queue,))

#     process1.start()
#     process2.start()

#     process1.join()
#     process2.join()