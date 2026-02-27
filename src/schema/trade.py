from pydantic import BaseModel


class TradeRequest(BaseModel):
    name: str


class TradeResponse(BaseModel):
    id: int = 1
    name: str = "John"

    class Config:
        from_attributes = True
