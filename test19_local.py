import asyncio
import time


async def async_api_get_user(user_id: int):
    """模拟异步接口：真实项目里可能是 aiohttp、异步数据库、消息队列。"""
    print(f"上游接口开始查询 user_id={user_id}")
    await asyncio.sleep(2)
    print(f"上游接口返回 user_id={user_id}")
    return {"id": user_id, "name": f"user-{user_id}"}


async def build_user_profile(user_id: int):
    """下游方法要等待异步上游，所以它自己也必须写成 async def。"""
    print(f"下游开始组装用户资料 user_id={user_id}")
    user = await async_api_get_user(user_id)
    profile = {
        "user": user,
        "level": "VIP" if user_id == 1 else "NORMAL",
    }
    print(f"下游组装完成 user_id={user_id}: {profile}")
    return profile


def wrong_sync_downstream(user_id: int):
    """普通函数不能 await，只能拿到协程对象，拿不到真正结果。"""
    coroutine_obj = async_api_get_user(user_id)
    print("普通函数直接调用异步上游，得到的是:", coroutine_obj)
    print("这不是接口结果，而是一个等待被 await 的协程对象。")
    coroutine_obj.close()


async def main():
    print("错误示例：普通函数不能真正等待异步上游")
    wrong_sync_downstream(1)
    print()

    print("正确示例 1：下游 async def 里 await 上游")
    start = time.perf_counter()
    await build_user_profile(1)
    end = time.perf_counter()
    print(f"单个异步调用耗时: {end - start:.2f}s")
    print()

    print("正确示例 2：多个下游协程可以一起等待异步上游")
    start = time.perf_counter()
    await asyncio.gather(
        build_user_profile(1),
        build_user_profile(2),
    )
    end = time.perf_counter()
    print(f"两个异步调用并发耗时: {end - start:.2f}s")


if __name__ == "__main__":
    asyncio.run(main())
