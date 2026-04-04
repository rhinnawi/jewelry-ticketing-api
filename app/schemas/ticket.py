"""
Ticket request/response schemas.

Defines Pydantic models for ticket-related API operations.
"""

from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr

from app.schemas.item import ItemCreate, ItemResponse
from app.utils import TicketPriority, TicketStatus


class TicketCreate(BaseModel):
    """
    Schema for creating a new ticket.

    Attributes:
        customer_name: Name of the customer.
        customer_phone: Customer phone number (optional).
        customer_email: Customer email address (optional).
        priority: Ticket priority level (defaults to STANDARD).
        deadline: Target completion date (optional).
        items: List of items to include in the ticket.
        total_quote: Total quoted price (optional).
        quote_itemized: Whether quote is itemized (defaults to False).
        notes: Additional notes (optional).
    """

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
    """
    Schema for updating an existing ticket.

    All fields are optional - only provided fields will be updated.

    Attributes:
        priority: New priority level (optional).
        status: New ticket status (optional).
        deadline: New target completion date (optional).
        notes: New notes (optional).
    """

    priority: Optional[TicketPriority] = None
    status: Optional[TicketStatus] = None
    deadline: Optional[date] = None
    notes: Optional[str] = None


class TicketResponse(BaseModel):
    """
    Schema for ticket API responses.

    Attributes:
        id: Ticket identifier.
        ticket_number: Human-readable ticket number.
        customer_name: Customer name.
        customer_phone: Customer phone number.
        customer_email: Customer email.
        created_by_id: ID of user who created the ticket.
        created_at: Timestamp of creation.
        updated_at: Timestamp of last update.
        status: Current ticket status.
        priority: Ticket priority level.
        deadline: Target completion date.
        notes: Additional notes.
        total_quote: Total quoted price.
        quote_itemized: Whether quote is itemized.
        items: List of items in the ticket.
    """

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

    model_config = {"from_attributes": True}
