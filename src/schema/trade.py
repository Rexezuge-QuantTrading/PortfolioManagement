from typing import Optional

from pydantic import BaseModel


class TradeRequest(BaseModel):
    securityCode: str
    price: int = 0
    quantity: int


class TradeResponse(BaseModel):
    tracking_id: str

    class Config:
        from_attributes = True


class TrackOrderByIdResponse(BaseModel):
    buy_sell_flag: str  # 买卖标志，例如：买入 / 卖出
    market: str  # 交易市场，例如：深A / 沪A
    price: float  # 委托价格
    entrust_id: str  # 委托序号
    quantity: int  # 委托数量
    date: str  # 委托日期 YYYYMMDD
    time: str  # 委托时间 HH:MM:SS
    deal_quantity: int  # 成交数量
    cancel_quantity: int  # 撤单数量
    status: str  # 状态说明，例如：已成 / 已撤
    shareholder_code: str  # 股东代码
    security_code: str  # 证券代码
    security_name: str  # 证券名称
