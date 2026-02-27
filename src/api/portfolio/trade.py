from fastapi import APIRouter, HTTPException, status
from schema.Trade import TradeRequest, TradeResponse

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
    response = TradeResponse()

    if not response:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User could not be created",
        )

    return response
