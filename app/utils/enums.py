from enum import Enum

class TicketStatus(str, Enum):
    DRAFT = "draft"
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class TicketPriority(str, Enum):
    STANDARD = "standard"
    RUSH = "rush"
    URGENT = "urgent"

class ItemType(str, Enum):
    RING = "ring"
    NECKLACE = "necklace"
    EARRING = "earring"
    BRACELET = "bracelet"
    WATCH = "watch"
    OTHER = "other"

class ItemStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    QUALITY_CHECK = "quality_check"

class UserRole(str, Enum):
    SALES = "sales"
    BENCH = "bench"
    ADMIN = "admin"
    