# encoding: utf-8
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from openai import AsyncOpenAI

load_dotenv()  # 从同目录的 .env 文件加载环境变量
DEEPSEEK_API_KEY = os.environ["DEEPSEEK_API_KEY"]  # 从环境变量读取，不要硬编码到代码里

client = AsyncOpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com",
)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


async def stream_deepseek(prompt: str):
    stream = await client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    async for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            yield f"data: {content}\n\n"
    yield "data: [DONE]\n\n"


@app.get("/")
async def index():
    return FileResponse("frontend.html")


@app.get("/chat")
async def chat(prompt: str):
    return StreamingResponse(stream_deepseek(prompt), media_type="text/event-stream")
