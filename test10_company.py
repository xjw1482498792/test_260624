from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items")
def read_item(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}    