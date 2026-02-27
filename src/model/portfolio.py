from pydantic import BaseModel
from typing import Optional


class Portfolio(BaseModel):
    id: int  # Hash Key
    symbol: str  # Sort Key
    quantity: int  # Retain 4 decimal places
    avgCostBasis: int  # Retain 8 decimal places
    lock: Optional[int] = None  # Unix Timestamp
    createdAt: int  # Unix Timestamp
    updatedAt: int  # Unix Timestamp

    class Config:
        from_attributes = True
