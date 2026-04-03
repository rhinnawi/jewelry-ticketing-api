from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Ticket
from app.schemas import TicketCreate, TicketResponse, TicketUpdate
from app.services import TicketService
from typing import List

router = APIRouter(prefix="/tickets", tags=["tickets"])
ticket_service = TicketService()

@router.post("/", response_model=TicketResponse)
async def create_ticket(
    ticket: TicketCreate,
    db: Session = Depends(get_db),
):
    """Create a new ticket (sales associate)"""
    return ticket_service.create_ticket(db, ticket, "user-id")

@router.get("/", response_model=List[TicketResponse])
async def list_tickets(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 50,
):
    """List all tickets"""
    tickets = db.query(Ticket).offset(skip).limit(limit).all()
    return tickets

@router.get("/queue", response_model=List[TicketResponse])
async def get_bench_queue(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 50,
):
    """Get queue sorted by priority (bench jeweler view)"""
    return ticket_service.get_queue(db, skip, limit)

@router.get("/{ticket_id}", response_model=TicketResponse)
async def get_ticket(
    ticket_id: str,
    db: Session = Depends(get_db),
):
    """Get a specific ticket"""
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@router.patch("/{ticket_id}", response_model=TicketResponse)
async def update_ticket(
    ticket_id: str,
    ticket_update: TicketUpdate,
    db: Session = Depends(get_db),
):
    """Update ticket"""
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    for key, value in ticket_update.dict(exclude_unset=True).items():
        setattr(ticket, key, value)
    
    db.commit()
    db.refresh(ticket)
    return ticket