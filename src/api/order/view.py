from dataclasses import asdict
from src.model.easytrader import Entrust
from fastapi import APIRouter, status
from src.schema.trade import TrackOrderByIdResponse
from src.util.helper.trade import TradeHelper

router: APIRouter = APIRouter()


@router.get(
    "/{tracking_id}",
    response_model=TrackOrderByIdResponse,
    status_code=status.HTTP_200_OK,
)
def track_order_by_id(tracking_id: str) -> TrackOrderByIdResponse:
    trader: TradeHelper = TradeHelper()
    entrust: Entrust = trader.checkEntrustById(tracking_id=tracking_id)
    return TrackOrderByIdResponse(**asdict(entrust))
