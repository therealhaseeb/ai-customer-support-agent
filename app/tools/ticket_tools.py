from sqlalchemy.orm import Session
from app.db import crud
from app.utils import errors
from app.services.logger import logger

def create_support_ticket(db: Session, user_id: int, issue: str):
    ticket = crud.create_ticket(db, user_id, issue)
    logger.info(f"Ticket created {ticket.id} for user {user_id}")
    return {"ticket_id": ticket.id, "status": ticket.status, "issue": ticket.issue}

def escalate_to_human(db: Session, ticket_id: int, reason: str):
    ticket = crud.update_ticket_status(db, ticket_id, "escalated")
    logger.info(f"Ticket {ticket_id} escalated due to: {reason}")
    return {"ticket_id": ticket.id, "status": ticket.status, "reason": reason}
