# encoding: utf-8
import asyncio


async def fake_llm_stream(prompt: str):
    words = f"你问的是：{prompt}。这是流式输出的回答，一个字一个字地出来。".split("。")
    for word in words:
        for char in word:
            yield f"data: {char}\n\n"
            await asyncio.sleep(0.1)
        yield f"data: 。\n\n"
        await asyncio.sleep(0.3)
    yield "data: [DONE]\n\n"

gen1 = fake_llm_stream("你好")

async def main():
    tmp = await anext(gen1)  # 输出第一个字
    print(tmp)
    tmp = await anext(gen1)  # 输出第二个字
    print(tmp)
    
asyncio.run(main())
