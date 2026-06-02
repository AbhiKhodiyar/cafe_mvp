from pydantic import BaseModel, Field

class IdentityExtractionSchema(BaseModel):
    item_name: str = Field(..., description="The matching identified supply name of the item.")

class InventoryLogResponse(BaseModel):
    item: str
    updated_stock: int