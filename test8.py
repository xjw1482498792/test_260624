from fastapi import FastAPI
from pydantic import BaseModel

from fastapi import FastAPI

app = FastAPI(
    title="我的 API",                    # API 标题
    description="这是一个示例 API，展示文档自定义功能",  # API 描述
    version="1.0.0",                    # API 版本
    terms_of_service="http://example.com/terms/",  # 服务条款 URL
    contact={                           # 联系信息
        "name": "开发者",
        "url": "http://example.com/contact/",
        "email": "dev@example.com",
    },
    license_info={                      # 许可证信息
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)
#GET
@app.get("/")
async def root():
    """根路径，返回欢迎信息"""
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    """根据 ID 获取条目，支持可选的查询参数 q"""
    return {"item_id": item_id, "q": q}

#POST
# 定义请求体数据模型
class Item(BaseModel):
    name: str           # 必填：商品名称
    description: str | None = None  # 可选：商品描述
    price: float        # 必填：商品价格
    tax: float | None = None        # 可选：税费
@app.post("/items/")
async def create_item(item: Item):
    return item

#PUT
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict() }