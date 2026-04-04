"""
SQLAlchemy ORM models.

Defines all database models for the jewelry ticketing system.
"""

import uuid
from datetime import datetime

from sqlalchemy import (Column, Date, DateTime, Enum,
                        Float, ForeignKey, Integer, String, Text, Boolean)
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.utils import ItemStatus, ItemType, TicketPriority, TicketStatus, UserRole


class User(Base):
    """
    User model for system users (sales associates, bench jewelers, admins).

    Attributes:
        id: Unique user identifier.
        username: Unique username.
        email: Unique email address.
        hashed_password: Hashed password for authentication.
        role: User role (sales, bench, admin).
        created_at: Timestamp of user creation.
        tickets: Relationship to tickets created by this user.
        items: Relationship to items assigned to this user.
    """

    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.SALES)
    created_at = Column(DateTime, default=datetime.utcnow)

    tickets = relationship("Ticket", back_populates="created_by")
    items = relationship("Item", back_populates="assigned_to")


class Ticket(Base):
    """
    Ticket model for job orders.

    Attributes:
        id: Unique ticket identifier.
        ticket_number: Human-readable ticket number.
        customer_name: Name of the customer.
        customer_phone: Customer phone number.
        customer_email: Customer email address.
        created_by_id: ID of user who created the ticket.
        created_at: Timestamp of ticket creation.
        updated_at: Timestamp of last update.
        status: Current status of the ticket.
        priority: Priority level of the ticket.
        deadline: Target completion date.
        notes: Additional notes about the ticket.
        total_quote: Total quoted price for all items.
        quote_itemized: Whether quote is itemized.
        created_by: Relationship to user who created ticket.
        items: Relationship to items in this ticket.
    """

    __tablename__ = "tickets"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    ticket_number = Column(String, unique=True, nullable=False, index=True)
    customer_name = Column(String, nullable=False)
    customer_phone = Column(String)
    customer_email = Column(String)
    created_by_id = Column(String, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)
    status = Column(Enum(TicketStatus), default=TicketStatus.DRAFT)
    priority = Column(Enum(TicketPriority), default=TicketPriority.STANDARD)
    deadline = Column(Date)
    notes = Column(Text)
    total_quote = Column(Float)
    quote_itemized = Column(Boolean, default=False)

    created_by = relationship("User", back_populates="tickets")
    items = relationship("Item", back_populates="ticket",
                         cascade="all, delete-orphan")


class Item(Base):
    """
    Item model for individual jewelry pieces in a ticket.

    Attributes:
        id: Unique item identifier.
        ticket_id: ID of parent ticket.
        item_type: Type of jewelry (ring, necklace, etc).
        description: Description of the item and work needed.
        quantity: Number of this item.
        quote_price: Quoted price for this item.
        status: Current status of the item.
        assigned_to_id: ID of user assigned to this item.
        notes: Additional notes about the item.
        created_at: Timestamp of item creation.
        ticket: Relationship to parent ticket.
        assigned_to: Relationship to assigned user.
    """

    __tablename__ = "items"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    ticket_id = Column(String, ForeignKey("tickets.id", ondelete="CASCADE"))
    item_type = Column(Enum(ItemType), nullable=False)
    description = Column(Text)
    quantity = Column(Integer, default=1)
    quote_price = Column(Float)
    status = Column(Enum(ItemStatus), default=ItemStatus.PENDING)
    assigned_to_id = Column(String, ForeignKey("users.id"))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    ticket = relationship("Ticket", back_populates="items")
    assigned_to = relationship("User", back_populates="items")


class PriorityAudit(Base):
    """
    Audit log for priority changes.

    Attributes:
        id: Unique audit record identifier.
        ticket_id: ID of the ticket whose priority changed.
        old_priority: Previous priority level.
        new_priority: New priority level.
        changed_by_id: ID of user who made the change.
        reason: Reason for the priority change.
        changed_at: Timestamp of the change.
    """

    __tablename__ = "priority_audit"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    ticket_id = Column(String, ForeignKey("tickets.id"))
    old_priority = Column(Enum(TicketPriority))
    new_priority = Column(Enum(TicketPriority))
    changed_by_id = Column(String, ForeignKey("users.id"))
    reason = Column(Text)
    changed_at = Column(DateTime, default=datetime.utcnow)
