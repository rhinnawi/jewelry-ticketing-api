"""
Ticket business logic service.

Handles ticket creation, retrieval, updates, and queue management.
"""

import uuid
from datetime import datetime

from sqlalchemy.orm import Session

from app.db.models import PriorityAudit, Ticket
from app.schemas import TicketCreate, TicketResponse, TicketUpdate
from app.utils import TicketPriority, TicketStatus

from .priority_service import PriorityService


class TicketService:
    """Service for ticket-related business logic."""

    @staticmethod
    def create_ticket(db: Session, ticket_data: TicketCreate, user_id: str) -> Ticket:
        """
        Create a new ticket with associated items.

        Args:
            db: Database session.
            ticket_data: Ticket creation data.
            user_id: ID of user creating the ticket.

        Returns:
            Ticket: Created ticket object.
        """
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
            quote_itemized=1 if ticket_data.quote_itemized else 0,
            notes=ticket_data.notes,
            created_by_id=user_id,
        )

        db.add(ticket)
        db.commit()
        db.refresh(ticket)
        return ticket

    @staticmethod
    def get_queue(db: Session, skip: int = 0, limit: int = 50) -> list[Ticket]:
        """
        Get queue of pending/in-progress tickets sorted by priority.

        Args:
            db: Database session.
            skip: Number of records to skip (pagination).
            limit: Maximum number of records to return.

        Returns:
            list[Ticket]: List of tickets sorted by priority score.
        """
        tickets = db.query(Ticket).filter(
            Ticket.status.in_([TicketStatus.PENDING, TicketStatus.IN_PROGRESS])
        ).all()

        priority_service = PriorityService()
        tickets_with_scores = [
            (ticket, priority_service.calculate_priority_score(ticket))
            for ticket in tickets
        ]

        tickets_sorted = sorted(
            tickets_with_scores, key=lambda x: (-x[1], x[0].created_at)
        )

        return [ticket for ticket, _ in tickets_sorted[skip: skip + limit]]

    @staticmethod
    def update_priority(
        db: Session, ticket_id: str, new_priority: str, reason: str, user_id: str
    ) -> Ticket | None:
        """
        Update ticket priority and create audit log.

        Args:
            db: Database session.
            ticket_id: ID of ticket to update.
            new_priority: New priority level.
            reason: Reason for the priority change.
            user_id: ID of user making the change.

        Returns:
            Ticket | None: Updated ticket or None if not found.
        """
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
    def update_status(db: Session, ticket_id: str, new_status: str) -> Ticket | None:
        """
        Update ticket status.

        Args:
            db: Database session.
            ticket_id: ID of ticket to update.
            new_status: New status value.

        Returns:
            Ticket | None: Updated ticket or None if not found.
        """
        ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

        if not ticket:
            return None

        ticket.status = TicketStatus(new_status)
        db.commit()
        db.refresh(ticket)
        return ticket
