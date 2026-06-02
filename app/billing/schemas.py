from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, List
from app.ordering.schemas import OrderItem

class DiscountType(str, Enum):
    PERCENTAGE = "percentage"
    FIXED = "fixed"

class DiscountRule(BaseModel):
    type: DiscountType
    value: float = Field(..., ge=0.0)

class InvoiceRequest(BaseModel):
    order_id: str
    items: List[OrderItem]
    tax_percentage: float = Field(default=5.0, ge=0.0, le=100.0)
    discount: Optional[DiscountRule] = None

class InvoiceResponse(BaseModel):
    order_id: str
    subtotal: float
    discount_applied: float
    tax_applied: float
    total_due: float