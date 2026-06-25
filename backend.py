# encoding: utf-8
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from openai import AsyncOpenAI

DEEPSEEK_API_KEY = "sk-83617bbf2f414149b59cce7be50f1c4b"  # 替换成你的 Key

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
