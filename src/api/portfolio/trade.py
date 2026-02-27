from decimal import Decimal
from fastapi import APIRouter, HTTPException, status
from src.schema.portfolios import GetPortfolioResponse
from src.schema.trade import TradeRequest, TradeResponse
from src.repository.portfolio import PortfolioRepository
from src.core.config import settings
from src.model.portfolio import Portfolio
from typing import List
from src.util.price import PriceUtil

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
        if "000000.CASH" == p.symbol:
            availableCash = Decimal(p.quantity)
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
    request: TradeRequest,
) -> TradeResponse:
    print(f"request: {request}")
    user: RemoteClient = use(
        "ths", host="127.0.0.1", port=1430
    )  # pyright: ignore[reportUnknownVariableType]
    # user.prepare(
    #     user='资金账号',
    #     password='交易密码',
    #     exe_path=r'C:\同花顺路径\xiadan.exe'  # 同花顺下单程序路径
    # )
    # # 买入
    # user.buy('600000', price=10.5, amount=100)

    # # 卖出
    # user.sell('600000', price=10.8, amount=100)
    response = TradeResponse()

    if not response:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User could not be created",
        )

    return response
