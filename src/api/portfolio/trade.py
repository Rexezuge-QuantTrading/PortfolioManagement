from fastapi import APIRouter, HTTPException, status
from src.schema.trade import TradeRequest, TradeResponse
from easytrader.remoteclient import RemoteClient, use  # type: ignore

router: APIRouter = APIRouter()


@router.post(
    "/{portfolio_id}/trade",
    response_model=TradeResponse,
    status_code=status.HTTP_200_OK,
)
def trade(
    request: TradeRequest,
) -> TradeResponse:
    """
    Create a new user.
    """
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
