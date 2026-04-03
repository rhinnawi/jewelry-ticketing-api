"""
Item request/response schemas.

Defines Pydantic models for item-related API operations.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.utils import ItemStatus, ItemType


class ItemCreate(BaseModel):
    """
    Schema for creating a new item.
    
    Attributes:
        item_type: Type of jewelry item.
        description: Description of the item and work needed.
        quantity: Number of items (defaults to 1).
        quote_price: Quoted price for this item (optional).
        notes: Additional notes (optional).
    """

    item_type: ItemType
    description: str
    quantity: int = 1
    quote_price: Optional[float] = None
    notes: Optional[str] = None


class ItemResponse(BaseModel):
    """
    Schema for item API responses.
    
    Attributes:
        id: Item identifier.
        ticket_id: Parent ticket identifier.
        item_type: Type of jewelry item.
        description: Description of the item.
        quantity: Number of items.
        quote_price: Quoted price.
        status: Current status of the item.
        assigned_to_id: ID of assigned user (if any).
        notes: Additional notes.
        created_at: Timestamp of creation.
    """

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

    model_config = {"from_attributes": True}