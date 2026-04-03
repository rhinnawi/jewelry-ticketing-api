from sqlalchemy import Column, String, Integer, DateTime, Float, Boolean, ForeignKey, Enum, Text, JSON, Date
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.db.database import Base
from app.utils import TicketStatus, TicketPriority, ItemType, ItemStatus, UserRole

class User(Base):
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
    __tablename__ = "tickets"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    ticket_number = Column(String, unique=True, nullable=False, index=True)
    customer_name = Column(String, nullable=False)
    customer_phone = Column(String)
    customer_email = Column(String)
    created_by_id = Column(String, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = Column(Enum(TicketStatus), default=TicketStatus.DRAFT)
    priority = Column(Enum(TicketPriority), default=TicketPriority.STANDARD)
    deadline = Column(Date)
    notes = Column(Text)
    total_quote = Column(Float)
    quote_itemized = Column(Boolean, default=False)
    
    created_by = relationship("User", back_populates="tickets")
    items = relationship("Item", back_populates="ticket", cascade="all, delete-orphan")

class Item(Base):
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
    __tablename__ = "priority_audit"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    ticket_id = Column(String, ForeignKey("tickets.id"))
    old_priority = Column(Enum(TicketPriority))
    new_priority = Column(Enum(TicketPriority))
    changed_by_id = Column(String, ForeignKey("users.id"))
    reason = Column(Text)
    changed_at = Column(DateTime, default=datetime.utcnow)