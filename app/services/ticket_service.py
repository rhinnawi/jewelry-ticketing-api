from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.db.models import Ticket, Item, User, PriorityAudit
from app.schemas import TicketCreate, TicketResponse, TicketUpdate
from app.utils import TicketStatus, TicketPriority
from app.services.priority_service import PriorityService
import uuid
from datetime import datetime

class TicketService:
    @staticmethod
    def create_ticket(db: Session, ticket_data: TicketCreate, user_id: str) -> Ticket:
        """Create a new ticket with items"""
        ticket_number = f"TKT-{int(datetime.utcnow().timestamp())}"
        
        ticket = Ticket(
            id=str(uuid.uuid4()),
            ticket_number=ticket_number,
            customer_name=ticket_data.customer_name,
            customer_phone=ticket_data.customer_phone,
            customer_email=ticket_data.customer_email,
            priority=ticket_data.priority,
            deadline=ticket_data.deadline,
            total_quote=ticket_data.total_quote,
            quote_itemized=ticket_data.quote_itemized,
            notes=ticket_data.notes,
            created_by_id=user_id,
        )
        
        for item_data in ticket_data.items:
            item = Item(
                id=str(uuid.uuid4()),
                item_type=item_data.item_type,
                description=item_data.description,
                quantity=item_data.quantity,
                quote_price=item_data.quote_price,
                notes=item_data.notes,
            )
            ticket.items.append(item)
        
        db.add(ticket)
        db.commit()
        db.refresh(ticket)
        return ticket
    
    @staticmethod
    def get_queue(db: Session, skip: int = 0, limit: int = 50):
        """Get queue sorted by priority score"""
        tickets = db.query(Ticket).filter(
            Ticket.status.in_([TicketStatus.PENDING, TicketStatus.IN_PROGRESS])
        ).all()
        
        priority_service = PriorityService()
        tickets_with_scores = [
            (ticket, priority_service.calculate_priority_score(ticket))
            for ticket in tickets
        ]
        
        tickets_sorted = sorted(
            tickets_with_scores,
            key=lambda x: (-x[1], x[0].created_at)
        )
        
        return [ticket for ticket, _ in tickets_sorted[skip:skip + limit]]
    
    @staticmethod
    def update_priority(
        db: Session,
        ticket_id: str,
        new_priority: str,
        reason: str,
        user_id: str
    ) -> Ticket:
        """Update ticket priority and log change"""
        ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
        
        if not ticket:
            return None
        
        old_priority = ticket.priority
        ticket.priority = TicketPriority(new_priority)
        
        audit = PriorityAudit(
            id=str(uuid.uuid4()),
            ticket_id=ticket_id,
            old_priority=old_priority,
            new_priority=ticket.priority,
            changed_by_id=user_id,
            reason=reason,
        )
        
        db.add(audit)
        db.commit()
        db.refresh(ticket)
        return ticket
    
    @staticmethod
    def update_status(db: Session, ticket_id: str, new_status: str) -> Ticket:
        """Update ticket status"""
        ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
        
        if not ticket:
            return None
        
        ticket.status = TicketStatus(new_status)
        db.commit()
        db.refresh(ticket)
        return ticket