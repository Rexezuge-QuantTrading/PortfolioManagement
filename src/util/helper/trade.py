# pyright: reportUnknownVariableType=false
# pyright: reportUnknownMemberType=false
# pyright: reportMissingTypeStubs=false
from easytrader.remoteclient import (
    RemoteClient,
    use,
)
from decimal import Decimal
from src.model.easytrader import Entrust


class FakeClient:
    def buy(self, _1, price, amount):
        return {"entrust_no": "11111111", "success": True}

    today_entrusts = [
        {
            "买卖标志": "买入",
            "交易市场": "深A",
            "委托价格": 0.627,
            "委托序号": "111111",
            "委托数量": 100,
            "委托日期": "20170313",
            "委托时间": "09:50:30",
            "成交数量": 100,
            "撤单数量": 0,
            "状态说明": "已成",
            "股东代码": "xxxxx",
            "证券代码": "162411",
            "证券名称": "华宝油气",
        },
        {
            "买卖标志": "买入",
            "交易市场": "深A",
            "委托价格": 0.6,
            "委托序号": "1111",
            "委托数量": 100,
            "委托日期": "20170313",
            "委托时间": "09:40:30",
            "成交数量": 0,
            "撤单数量": 100,
            "状态说明": "已撤",
            "股东代码": "xxx",
            "证券代码": "162411",
            "证券名称": "华宝油气",
        },
    ]


class TradeHelper:
    _client: RemoteClient

    def __init__(self):
        # self._client = use("ths", host="127.0.0.1", port=1430)
        self._client = FakeClient()

    def buy(self, securityCode: str, price: Decimal, quantity: int) -> str:
        result = self._client.buy(securityCode, price=float(price), amount=quantity)
        if not result.get("success", False):
            raise Exception(f"Buy failed: {result.get('message')}")
        return result.get("entrust_no", "")

    def getEntrusts(self):
        return self._client.today_entrusts

    def checkEntrustById(self, tracking_id: str) -> Entrust:
        # 获取当日所有委托记录
        today_entrusts = self.getEntrusts()

        # 场景1：无当日委托数据
        if not today_entrusts:
            raise ValueError("No entrust records found for today.")

        # 遍历所有委托记录
        for entrust in today_entrusts:
            # 数据结构健壮性检查
            if not isinstance(entrust, dict):
                raise RuntimeError("Invalid entrust data format detected.")

            # 精确匹配委托序号
            if entrust.get("委托序号") == tracking_id:
                return Entrust.from_dict(entrust)

        # 场景2：未找到匹配记录
        raise ValueError(f"Entrust record with ID {tracking_id} not found.")

    @staticmethod
    def getValidatedSecurityCode(securityCode: str) -> str:
        if len(securityCode) < 6:
            raise ValueError("输入字符串长度必须至少为6位。")
        truncated: str = securityCode[:6]
        if not truncated.isdigit():
            raise ValueError("前6位字符必须全部为数字 ('0'-'9')。")
        return truncated
