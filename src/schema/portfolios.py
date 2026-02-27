from decimal import Decimal
from pydantic import BaseModel
from typing import List


class ListPortfoliosRequest(BaseModel):
    limits: int = 100


class ListPortfoliosResponse(BaseModel):
    class Portfolio(BaseModel):
        id: int
        totalValues: Decimal

    portfolios: List[Portfolio]
