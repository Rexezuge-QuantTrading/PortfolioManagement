from decimal import Decimal
from pydantic import BaseModel
from typing import List


class GetPortfolioResponse(BaseModel):
    class Position(BaseModel):
        symbol: str
        quantity: float
        avgCostBasis: float

    type: str = "stock"

    # cash
    availableCash: float = 0.0

    # positions
    longPositions: List[Position] = []
    shortPositions: List[Position] = []

    # values
    totalValue: float = 0.0
    positionsValue: float = 0.0

    class Config:
        arbitrary_types_allowed = True


class ListPortfoliosRequest(BaseModel):
    limits: int = 100


class ListPortfoliosResponse(BaseModel):
    class Portfolio(BaseModel):
        id: int
        totalValue: float = 0.0

    portfolios: List[Portfolio]
