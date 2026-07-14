import asyncio
import time


def sync_fetch_data(name: str, count: int, delay: float):
    """普通生成器：模拟从一个数据源逐条拉取数据。"""
    for i in range(1, count + 1):
        time.sleep(delay)
        yield f"[{name}] 第 {i} 条数据"


async def async_fetch_data(name: str, count: int, delay: float):
    """异步生成器：模拟从一个数据源逐条拉取数据。"""
    for i in range(1, count + 1):
        await asyncio.sleep(delay)
        yield f"[{name}] 第 {i} 条数据"


def run_sync_demo():
    print("普通生成器 demo:")
    start = time.perf_counter()

    # 两个生成器只能一个接一个消费。A 等待时，B 不能执行。
    for item in sync_fetch_data("A", count=3, delay=1):
        print(item)

    for item in sync_fetch_data("B", count=3, delay=1):
        print(item)

    end = time.perf_counter()
    print(f"普通生成器总耗时: {end - start:.2f}s")
    print()


async def consume_async_generator(name: str):
    async for item in async_fetch_data(name, count=3, delay=1):
        print(item)


async def run_async_demo():
    print("异步生成器 demo:")
    start = time.perf_counter()

    # 两个异步生成器可以并发消费。A 等待 IO 时，B 可以继续推进。
    await asyncio.gather(
        consume_async_generator("A"),
        consume_async_generator("B"),
    )

    end = time.perf_counter()
    print(f"异步生成器总耗时: {end - start:.2f}s")
    print()


async def main():
    run_sync_demo()
    await run_async_demo()

    print("结论:")
    print("普通生成器遇到 time.sleep 会阻塞，只能串行等待。")
    print("异步生成器遇到 await 会让出控制权，等待期间可以运行其他协程。")
    print("所以优势不是不用等待，而是等待 IO 的时间可以被其他任务利用。")


if __name__ == "__main__":
    asyncio.run(main())
