# from celery import Celery

# app = Celery(
#     "tasks",
#     broker="redis://localhost:6379/0"
# )

# @app.task
# def add(x, y):
#     return x + y

import asyncio
import time


def sync_task1():
    print("sync task1 start")
    time.sleep(3)
    print("sync task1 end")


def sync_task2():
    print("sync task2 start")
    time.sleep(3)
    print("sync task2 end")


async def task1():
    print("task1 start")
    await asyncio.sleep(3)
    print("task1 end")


async def task2():
    print("task2 start")
    await asyncio.sleep(3)
    print("task2 end")


async def main():
    print("sync demo:")
    sync_start = time.perf_counter()
    sync_task1()
    sync_task2()
    sync_end = time.perf_counter()
    print(f"sync total time: {sync_end - sync_start:.2f}s")
    print()

    print("async demo:")
    start = time.perf_counter()
    await asyncio.gather(task1(), task2())
    end = time.perf_counter()
    print(f"async total time: {end - start:.2f}s")


asyncio.run(main())
