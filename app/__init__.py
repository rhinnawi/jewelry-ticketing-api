"""
Application initialization module.

Exports core application components for easy importing.
"""

from app.config import settings
from app.db.database import engine, SessionLocal

__all__ = ["settings", "engine", "SessionLocal"]