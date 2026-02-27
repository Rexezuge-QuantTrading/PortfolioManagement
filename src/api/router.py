from fastapi import APIRouter
from src.api.portfolio import trade
from src.api.portfolios import manage

router: APIRouter = APIRouter()
router.include_router(trade.router, prefix="/portfolio", tags=["portfolio"])
router.include_router(manage.router, prefix="/portfolios", tags=["portfolios"])
