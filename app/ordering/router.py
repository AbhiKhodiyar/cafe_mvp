from fastapi import APIRouter, HTTPException, status
from app.ordering.schemas import OrderCreate, OrderResponse, OrderStatus
from app.ordering.service import ordering_service

router = APIRouter()

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(payload: OrderCreate):
    return ordering_service.create_order(payload)

@router.patch("/{order_id}/status", response_model=OrderResponse)
async def update_order_status(order_id: str, target_status: OrderStatus):
    try:
        return ordering_service.transition_status(order_id, target_status)
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))