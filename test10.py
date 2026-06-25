# encoding: utf-8
import asyncio
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

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
