from decimal import Decimal
from fastapi import APIRouter, status
from src.schema.portfolios import GetPortfolioResponse
from src.schema.trade import TradeRequest, TradeResponse
from src.repository.portfolio import PortfolioRepository
from src.core.config import settings
from src.model.portfolio import Portfolio
from typing import List
from src.util.price import PriceUtil
from src.core.constants import CASH_SYMBOL
from src.util.helper.trade import TradeHelper

router: APIRouter = APIRouter()


@router.get(
    "/{portfolio_id}",
    response_model=GetPortfolioResponse,
    status_code=status.HTTP_200_OK,
)
def get_portfolio(
    portfolio_id: int,
) -> GetPortfolioResponse:
    portfolio_repository: PortfolioRepository = PortfolioRepository(
        settings.portfolio_table, settings.aws_region
    )
    positions: List[Portfolio] = portfolio_repository.getPortfoliosById(portfolio_id)
    response: GetPortfolioResponse = GetPortfolioResponse()
    availableCash: Decimal = Decimal(0)
    positionsValue: Decimal = Decimal(0)
    for p in positions:
        if CASH_SYMBOL == p.symbol:
            availableCash = PriceUtil.getActualQuantity(p.quantity)
            continue
        position = GetPortfolioResponse.Position(
            symbol=p.symbol,
            quantity=float(PriceUtil.getActualQuantity(p.quantity)),
            avgCostBasis=float(PriceUtil.getActualCostBasis(p.avgCostBasis)),
        )
        if p.quantity > 0:
            response.longPositions.append(position)
        else:
            response.shortPositions.append(position)
        positionsValue += PriceUtil.getActualSecurityValue(p.quantity, p.avgCostBasis)

    response.availableCash = float(availableCash)
    response.positionsValue = float(positionsValue)
    response.totalValue = float(availableCash + positionsValue)
    return response


@router.post(
    "/{portfolio_id}/trade",
    response_model=TradeResponse,
    status_code=status.HTTP_200_OK,
)
def trade(
    portfolio_id: int,
    request: TradeRequest,
) -> TradeResponse:
    securityCode: str = TradeHelper.getValidatedSecurityCode(request.securityCode)
    price: Decimal = Decimal(request.price) / Decimal(100)
    quantity: int = request.quantity
    trader: TradeHelper = TradeHelper()
    tracking_id: str = trader.buy(securityCode, price, quantity)
    response = TradeResponse(tracking_id=tracking_id)
    return response
