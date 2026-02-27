from fastapi import APIRouter
from api.portfolio import trade

router: APIRouter = APIRouter()
router.include_router(trade.router, prefix="/portfolio", tags=["portfolio"])
