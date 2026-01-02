from sqlalchemy.orm import Session
from app.db import models
from app.utils import errors

# ------------------------
# User CRUD
# ------------------------
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user(db: Session, name: str, email: str):
    user = models.User(name=name, email=email)
    if user:
        return user
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# ------------------------
# Order CRUD
# ------------------------
def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()


def create_order(db: Session, user_id: int, product_name: str, amount: float):
    order = models.Order(user_id=user_id, product_name=product_name, amount=amount)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def update_order_status(db: Session, order_id: int, status: str):
    order = get_order(db, order_id)
    if not order:
        raise errors.ToolExecutionError(f"Order {order_id} not found")
    order.status = status
    db.commit()
    db.refresh(order)
    return order


def mark_order_refunded(db: Session, order_id: int):
    order = get_order(db, order_id)
    if not order:
        raise errors.ToolExecutionError(f"Order {order_id} not found")
    order.refunded = True
    db.commit()
    db.refresh(order)
    return order


# ------------------------
# Ticket CRUD
# ------------------------
def create_ticket(db: Session, user_id: int, issue: str):
    ticket = models.Ticket(user_id=user_id, issue=issue)
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket


def update_ticket_status(db: Session, ticket_id: int, status: str):
    ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if not ticket:
        raise errors.ToolExecutionError(f"Ticket {ticket_id} not found")
    ticket.status = status
    db.commit()
    db.refresh(ticket)
    return ticket
