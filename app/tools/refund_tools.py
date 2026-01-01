from sqlalchemy.orm import Session
from app.db import crud
from app.utils import errors
from app.services.logger import logger

def check_refund_eligibility(db: Session, order_id: int, max_days: int = 30):
    """
    Check if refund is allowed based on status & mock policy
    """
    order = crud.get_order(db, order_id)
    if not order:
        raise errors.ToolExecutionError(f"Order {order_id} not found")
    
    if order.refunded:
        raise errors.RefundNotAllowedError(f"Order {order_id} is already refunded")
    
    if order.status != "delivered":
        raise errors.RefundNotAllowedError(f"Order {order_id} is not delivered yet")
    
    # In real RAG, retrieve actual policy
    logger.info(f"Order {order_id} eligible for refund")
    return True

def process_refund(db: Session, order_id: int):
    """
    Mark order as refunded
    """
    if check_refund_eligibility(db, order_id):
        order = crud.mark_order_refunded(db, order_id)
        logger.info(f"Refund processed for order {order_id}")
        return {"order_id": order.id, "refunded": order.refunded}
