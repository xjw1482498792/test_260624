# encoding: utf-8
import asyncio
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from time import sleep

app = FastAPI()


async def fake_llm_stream(prompt: str):
    words = f"你问的是：{prompt}。这是流式输出的回答，一个字一个字地出来。".split("。")
    for word in words:
        for char in word:
            yield f"data: {char}\n\n"
            await asyncio.sleep(0.1)
        yield f"data: 。\n\n"
        await asyncio.sleep(0.3)
    yield "data: [DONE]\n\n"


@app.get("/stream")
async def stream(prompt: str = "你好"):
    return StreamingResponse(fake_llm_stream(prompt), media_type="text/event-stream")

#我的测试
# @app.get("/my_stream")
# async def my_stream(prompt: str = "你好"):

#自定义流式输出
async def fake_llm_stream2(prompt: str):
    words = f"你问的是：{prompt}。这是流式输出的回答，一个字一个字地出来。".split("。")
    for word in words:
        for char in word:
            yield f"{char}"
            await asyncio.sleep(0.1)
        yield f"。\n\n"
        await asyncio.sleep(0.3)
    yield "[DONE]\n\n"

#异步生成器
gen = fake_llm_stream2("你好")
async def print_stream(gen):
    async for chunk in gen:
        print(chunk, end='', flush=True)

asyncio.run(gen)