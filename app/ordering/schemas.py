from enum import Enum
from pydantic import BaseModel, Field
from typing import List

class OrderStatus(str, Enum):
    PENDING = "pending"
    PREPARING = "preparing"
    DONE = "done"

class OrderItem(BaseModel):
    item_name: str = Field(..., min_length=1, examples=["Arabica Beans"])
    quantity: int = Field(..., gt=0, examples=[2])
    unit_price: float = Field(..., gt=0.0, examples=[15.00])

class OrderCreate(BaseModel):
    items: List[OrderItem]

class OrderResponse(BaseModel):
    id: str
    status: OrderStatus
    items: List[OrderItem]