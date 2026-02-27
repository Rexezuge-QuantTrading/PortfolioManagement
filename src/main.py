from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "ok"}

@app.get("/hello/{name}")
async def hello(name: str):
    return {"message": f"Hello {name}"}

# Lambda 入口
handler = Mangum(app)
