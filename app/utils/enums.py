"""
Enumeration definitions for the application.

Defines all enum types used across the API for consistency and type safety.
"""
from enum import Enum


class TicketStatus(str, Enum):
    """Status states for a ticket."""
    DRAFT = "draft"
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class TicketPriority(str, Enum):
    """Priority levels for tickets."""
    STANDARD = "standard"
    RUSH = "rush"
    URGENT = "urgent"


class ItemType(str, Enum):
    """Types of jewelry items."""
    RING = "ring"
    NECKLACE = "necklace"
    EARRING = "earring"
    BRACELET = "bracelet"
    WATCH = "watch"
    OTHER = "other"


class ItemStatus(str, Enum):
    """Status states for individual items."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    QUALITY_CHECK = "quality_check"


class UserRole(str, Enum):
    """User roles in the system."""
    SALES = "sales"
    BENCH = "bench"
    ADMIN = "admin"
