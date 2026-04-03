from pydantic import BaseModel
from app.utils import ItemType, ItemStatus
from datetime import datetime
from typing import Optional

class ItemCreate(BaseModel):
    item_type: ItemType
    description: str
    quantity: int = 1
    quote_price: Optional[float] = None
    notes: Optional[str] = None

class ItemResponse(BaseModel):
    id: str
    ticket_id: str
    item_type: ItemType
    description: str
    quantity: int
    quote_price: Optional[float]
    status: ItemStatus
    assigned_to_id: Optional[str]
    notes: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True