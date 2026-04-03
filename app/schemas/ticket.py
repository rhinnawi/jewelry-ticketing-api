from pydantic import BaseModel, EmailStr
from app.utils import TicketStatus, TicketPriority
from app.schemas.item import ItemCreate, ItemResponse
from datetime import date, datetime
from typing import Optional, List

class TicketCreate(BaseModel):
    customer_name: str
    customer_phone: Optional[str] = None
    customer_email: Optional[EmailStr] = None
    priority: TicketPriority = TicketPriority.STANDARD
    deadline: Optional[date] = None
    items: List[ItemCreate]
    total_quote: Optional[float] = None
    quote_itemized: bool = False
    notes: Optional[str] = None

class TicketUpdate(BaseModel):
    priority: Optional[TicketPriority] = None
    status: Optional[TicketStatus] = None
    deadline: Optional[date] = None
    notes: Optional[str] = None

class TicketResponse(BaseModel):
    id: str
    ticket_number: str
    customer_name: str
    customer_phone: Optional[str]
    customer_email: Optional[str]
    created_by_id: str
    created_at: datetime
    updated_at: datetime
    status: TicketStatus
    priority: TicketPriority
    deadline: Optional[date]
    notes: Optional[str]
    total_quote: Optional[float]
    quote_itemized: bool
    items: List[ItemResponse]

    class Config:
        from_attributes = True