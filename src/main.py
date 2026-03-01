from fastapi import FastAPI
from mangum import Mangum
from src.api.router import router
from src.middleware.auth import AuthMiddleware
from src.core.config import settings

app: FastAPI = FastAPI()
app.add_middleware(AuthMiddleware, secret_key=settings.hmac_secret_key)


@app.get("/")
async def root():
    return {"status": "ok"}


app.include_router(router, prefix="/api")
handler: Mangum = Mangum(app)
