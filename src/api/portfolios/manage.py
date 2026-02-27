from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from src.schema.portfolios import ListPortfoliosRequest, ListPortfoliosResponse
from src.repository.portfolio import PortfolioRepository
from src.model.portfolio import Portfolio
from src.core.config import settings

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
    ret_portfolios_map: dict[int, ListPortfoliosResponse.Portfolio] = {}
    for p in portfolios:
        current_total_values = (
            Decimal(p.quantity) * Decimal(p.avgCostBasis) / Decimal(1_0000_0000)
        )
        if p.id in ret_portfolios_map:
            ret_portfolios_map[p.id].totalValues += current_total_values
        else:
            ret_portfolios_map[p.id] = ListPortfoliosResponse.Portfolio(
                id=p.id, totalValues=current_total_values
            )
    return ListPortfoliosResponse(portfolios=list(ret_portfolios_map.values()))
