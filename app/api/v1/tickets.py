"""
Ticket API endpoints.

Defines all routes for ticket-related operations.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Ticket
from app.schemas import TicketCreate, TicketResponse, TicketUpdate
from app.services import TicketService

router = APIRouter(prefix="/tickets", tags=["tickets"])
ticket_service = TicketService()


@router.post("/", response_model=TicketResponse, status_code=201)
async def create_ticket(
    ticket: TicketCreate,
    db: Session = Depends(get_db),
) -> TicketResponse:
    """
    Create a new ticket.
    
    This endpoint is used by sales associates to create new repair tickets.
    
    Args:
        ticket: Ticket data to create.
        db: Database session (injected).
        
    Returns:
        TicketResponse: Created ticket with all details.
        
    Raises:
        HTTPException: If there's an error creating the ticket.
    """
    return ticket_service.create_ticket(db, ticket, "user-id")


@router.get("/", response_model=List[TicketResponse])
async def list_tickets(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 50,
) -> List[TicketResponse]:
    """
    List all tickets.
    
    Retrieve paginated list of all tickets in the system.
    
    Args:
        db: Database session (injected).
        skip: Number of records to skip for pagination.
        limit: Maximum number of records to return.
        
    Returns:
        List[TicketResponse]: List of tickets.
    """
    tickets = db.query(Ticket).offset(skip).limit(limit).all()
    return tickets


@router.get("/queue", response_model=List[TicketResponse])
async def get_bench_queue(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 50,
) -> List[TicketResponse]:
    """
    Get the bench queue.
    
    Returns tickets sorted by priority for the bench jeweler.
    Higher priority tickets appear first.
    
    Args:
        db: Database session (injected).
        skip: Number of records to skip for pagination.
        limit: Maximum number of records to return.
        
    Returns:
        List[TicketResponse]: Prioritized list of tickets.
    """
    return ticket_service.get_queue(db, skip, limit)


@router.get("/{ticket_id}", response_model=TicketResponse)
async def get_ticket(
    ticket_id: str,
    db: Session = Depends(get_db),
) -> TicketResponse:
    """
    Get a specific ticket by ID.
    
    Args:
        ticket_id: ID of the ticket to retrieve.
        db: Database session (injected).
        
    Returns:
        TicketResponse: Ticket details.
        
    Raises:
        HTTPException: 404 if ticket not found.
    """
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@router.patch("/{ticket_id}", response_model=TicketResponse)
async def update_ticket(
    ticket_id: str,
    ticket_update: TicketUpdate,
    db: Session = Depends(get_db),
) -> TicketResponse:
    """
    Update an existing ticket.
    
    Allows partial updates - only provided fields will be updated.
    
    Args:
        ticket_id: ID of the ticket to update.
        ticket_update: Fields to update.
        db: Database session (injected).
        
    Returns:
        TicketResponse: Updated ticket.
        
    Raises:
        HTTPException: 404 if ticket not found.
    """
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    for key, value in ticket_update.dict(exclude_unset=True).items():
        setattr(ticket, key, value)

    db.commit()
    db.refresh(ticket)
    return ticket