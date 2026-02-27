from decimal import Decimal
from fastapi import APIRouter, status, Depends
from typing import List
from src.schema.portfolios import ListPortfoliosRequest, ListPortfoliosResponse
from src.repository.portfolio import PortfolioRepository
from src.model.portfolio import Portfolio
from src.core.config import settings
from src.util.price import PriceUtil
from src.core.constants import CASH_SYMBOL

router: APIRouter = APIRouter()


@router.get(
    "/",
    response_model=ListPortfoliosResponse,
    status_code=status.HTTP_200_OK,
)
def list_portfolios(
    request: ListPortfoliosRequest = Depends(),
) -> ListPortfoliosResponse:
    portfolioRepository: PortfolioRepository = PortfolioRepository(
        settings.portfolio_table, settings.aws_region
    )
    portfolios: List[Portfolio] = portfolioRepository.get_all_portfolios()
    totalValues: dict[int, Decimal] = {}
    retPortfolios: dict[int, ListPortfoliosResponse.Portfolio] = {}
    for p in portfolios:
        currentValue: Decimal
        if CASH_SYMBOL == p.symbol:
            currentValue = PriceUtil.getActualQuantity(p.quantity)
        else:
            currentValue = PriceUtil.getActualSecurityValue(p.quantity, p.avgCostBasis)
        if p.id in totalValues:
            totalValues[p.id] += currentValue
        else:
            totalValues[p.id] = currentValue
            retPortfolios[p.id] = ListPortfoliosResponse.Portfolio(id=p.id)
        retPortfolios[p.id].totalValue = float(totalValues[p.id])

    return ListPortfoliosResponse(portfolios=list(retPortfolios.values()))
