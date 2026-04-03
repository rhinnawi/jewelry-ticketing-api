from datetime import datetime, date
from app.utils import TicketPriority

class PriorityService:
    @staticmethod
    def calculate_priority_score(ticket) -> int:
        """
        Returns a score (0-100) that determines queue position.
        Higher = more urgent.
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