# encoding: utf-8
"""
异步生成器作用演示
核心要点：异步生成器在「等待」(await) 的时候会让出控制权，
         于是多个生成器可以「并发」产出数据，而不是一个等完再等下一个。
运行：python test_async_gen_demo.py
"""
import asyncio
import time


# ============ 1. 一个异步生成器：模拟从某个数据源逐条拉数据 ============
async def fetch_data(name: str, count: int, delay: float):
    """模拟一个数据源：每隔 delay 秒吐出一条数据（比如等数据库/网络/LLM）"""
    for i in range(1, count + 1):
        await asyncio.sleep(delay)          # ← 关键：等待时让出控制权
        yield f"[{name}] 第 {i} 条数据"


# ============ 2. 串行消费：一个生成器消费完，再消费下一个 ============
async def run_serial():
    print("\n===== 串行消费（一个接一个） =====")
    start = time.perf_counter()

    async for item in fetch_data("数据源A", 3, 1.0):
        print(item)
    async for item in fetch_data("数据源B", 3, 1.0):
        print(item)

    print(f"串行总耗时：{time.perf_counter() - start:.1f} 秒")


# ============ 3. 并发消费：两个生成器同时产出 ============
async def consume(gen):
    async for item in gen:
        print(item)


async def run_concurrent():
    print("\n===== 并发消费（两个同时跑） =====")
    start = time.perf_counter()

    # 两个异步生成器同时消费：A 在等 1 秒的间隙，B 也在产出
    await asyncio.gather(
        consume(fetch_data("数据源A", 3, 1.0)),
        consume(fetch_data("数据源B", 3, 1.0)),
    )

    print(f"并发总耗时：{time.perf_counter() - start:.1f} 秒")


# ============ 4. 实战感：流式输出 + 同时干别的事 ============
async def llm_stream(prompt: str):
    """模拟 LLM 一个字一个字往外吐"""
    for ch in f"回答：{prompt} 已收到~":
        await asyncio.sleep(0.2)
        yield ch


async def heartbeat():
    """模拟服务器在 LLM 吐字的间隙还能干别的（比如打心跳/处理其他请求）"""
    for _ in range(5):
        await asyncio.sleep(0.5)
        print("   <后台心跳：服务器没闲着，还能处理其他任务>")


async def run_stream_demo():
    print("\n===== 流式输出的同时，后台还能干别的 =====")

    async def print_stream():
        async for ch in llm_stream("你好"):
            print(ch, end="", flush=True)
        print()

    await asyncio.gather(print_stream(), heartbeat())


async def main():
    await run_serial()       # 预计 ~6 秒（3+3）
    await run_concurrent()   # 预计 ~3 秒（并发，省一半）
    await run_stream_demo()  # 流式吐字 + 后台心跳交错出现


# if __name__ == "__main__":
#     asyncio.run(main())


#理解测试
fetch_gen = fetch_data("测试数据源", 3, 1.0)
async def put_value():
    value = await anext(fetch_gen)  # 生成器对象
    print(value)
    value = await anext(fetch_gen)  # 生成器对象
    print(value)    
asyncio.run(put_value())              