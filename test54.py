# #rlock没有例子

# import threading

# lock = threading.Lock()

# with lock:
#     print("lock")


# #线程池
# from concurrent.futures import ThreadPoolExecutor
# import time


# def task(number):
#     print(f"开始任务 {number}")
#     time.sleep(1)  # 模拟 I/O 等待
#     return number * 2


# if __name__ == "__main__":
#     with ThreadPoolExecutor(max_workers=3) as pool:
#         futures = [
#             pool.submit(task, number)
#             for number in range(5)
#         ]

#         for future in futures:
#             print("结果：", future.result())     


#进程
from concurrent.futures import ProcessPoolExecutor


def calculate(number):
    total = 0

    for value in range(number):
        total += value * value

    return total


if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers=4) as pool:
        futures = [
            pool.submit(calculate, number)
            for number in [1_000_000, 2_000_000, 3_000_000]
        ]

        for future in futures:
            print("结果：", future.result())            