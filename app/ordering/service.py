import uuid
from typing import Dict
from app.ordering.schemas import OrderStatus, OrderCreate

class OrderingService:
    def __init__(self):
        self._orders: Dict[str, dict] = {}

    def create_order(self, order_in: OrderCreate) -> dict:
        order_id = str(uuid.uuid4())
        new_order = {
            "id": order_id,
            "status": OrderStatus.PENDING,
            "items": [item.model_dump() for item in order_in.items]
        }
        self._orders[order_id] = new_order
        return new_order

    def transition_status(self, order_id: str, target_status: OrderStatus) -> dict:
        order = self._orders.get(order_id)
        if not order:
            raise ValueError(f"Order '{order_id}' not found.")
        
        current = order["status"]
        
        # State machine constraint verification [cite: 9]
        valid_transition = (
            (current == OrderStatus.PENDING and target_status == OrderStatus.PREPARING) or
            (current == OrderStatus.PREPARING and target_status == OrderStatus.DONE)
        )
        
        if not valid_transition:
            raise ValueError(f"Illegal transition: Cannot jump status from '{current}' directly to '{target_status}'.")
            
        order["status"] = target_status
        return order

ordering_service = OrderingService()