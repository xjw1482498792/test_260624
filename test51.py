from multiprocessing import Process


def task():
    print("执行任务")


if __name__ == "__main__":
    process = Process(target=task)
    process.start()
    process.join()


# print("-------------------------")    
# from threading import Thread


# def task():
#     print("执行任务")


# thread = Thread(target=task)
# thread.start()
# thread.join()

# print("-------------------------")    
# import asyncio


# async def task():
#     print("开始任务")
#     await asyncio.sleep(1)
#     print("结束任务")


# asyncio.run(task())