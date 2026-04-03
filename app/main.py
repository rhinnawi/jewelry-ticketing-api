"""
FastAPI application entry point.

Initializes the application, configures middleware, and registers routes.
"""

import uuid

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import items_router, tickets_router, users_router
from app.config import settings
from app.db.database import Base, engine
from app.db.models import User

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Jewelry Ticketing API",
    description="API for jewelry store repair ticketing system",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(tickets_router, prefix="/api/v1")
app.include_router(items_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")


@app.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    """
    Health check endpoint.
    
    Returns:
        dict: Status information.
    """
    return {"status": "ok"}


@app.get("/", tags=["root"])
async def root() -> dict[str, str]:
    """
    Root endpoint.
    
    Returns:
        dict: Welcome message.
    """
    return {"message": "Welcome to Jewelry Ticketing API"}