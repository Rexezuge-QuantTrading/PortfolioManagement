from fastapi import FastAPI
from mangum import Mangum
from api.router import router

app: FastAPI = FastAPI()


@app.get("/")
async def root():
    return {"status": "ok"}


app.include_router(router, prefix="/api")

# Lambda 入口
handler: Mangum = Mangum(app)
