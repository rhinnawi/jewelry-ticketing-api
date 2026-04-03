"""
Priority scoring and management service.

Handles priority calculations and queue ordering logic.
"""

from datetime import date, datetime

from app.utils import TicketPriority


class PriorityService:
    """Service for calculating and managing ticket priorities."""

    @staticmethod
    def calculate_priority_score(ticket) -> int:
        """
        Calculate priority score for a ticket.
        
        Higher scores indicate more urgent tickets. Score is based on:
        - Base priority level (standard=10, rush=50, urgent=85)
        - Days until deadline
        
        Args:
            ticket: Ticket object to score.
            
        Returns:
            int: Priority score (0-100).
        """
        base_score = {
            TicketPriority.STANDARD: 10,
            TicketPriority.RUSH: 50,
            TicketPriority.URGENT: 85,
        }.get(ticket.priority, 10)

        if not ticket.deadline:
            return base_score

        days_until_deadline = (ticket.deadline - date.today()).days

        if days_until_deadline <= 0:
            return 100
        elif days_until_deadline == 1:
            return base_score + 40
        elif days_until_deadline <= 3:
            return base_score + 20
        elif days_until_deadline <= 7:
            return base_score + 10

        return base_score