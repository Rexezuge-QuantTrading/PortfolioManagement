from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Entrust:
    """
    强类型委托数据模型
    """

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

    @staticmethod
    def from_dict(data: dict) -> "Entrust":
        """
        从接口返回的字典构建 Entrust 对象

        :param data: 接口原始字典
        :return: Entrust 实例
        :raises ValueError: 字段缺失或类型异常
        """

        try:
            return Entrust(
                buy_sell_flag=str(data["买卖标志"]),
                market=str(data["交易市场"]),
                price=float(data["委托价格"]),
                entrust_id=str(data["委托序号"]),
                quantity=int(data["委托数量"]),
                date=str(data["委托日期"]),
                time=str(data["委托时间"]),
                deal_quantity=int(data["成交数量"]),
                cancel_quantity=int(data["撤单数量"]),
                status=str(data["状态说明"]),
                shareholder_code=str(data["股东代码"]),
                security_code=str(data["证券代码"]),
                security_name=str(data["证券名称"]),
            )
        except KeyError as e:
            raise ValueError(f"Missing required entrust field: {e}") from e
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid entrust field type: {e}") from e
