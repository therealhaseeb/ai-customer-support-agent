from sqlalchemy.orm import Session
from app.db import crud
from app.utils import errors
from app.services.logger import logger

def get_order_status(db: Session, order_id: int):
    order = crud.get_order(db, order_id)
    if not order:
        raise errors.ToolExecutionError(f"Order {order_id} not found")
    logger.info(f"Order {order_id} status: {order.status}")
    return {"order_id": order.id, "status": order.status, "refunded": order.refunded}

def get_order_details(db: Session, order_id: int):
    order = crud.get_order(db, order_id)
    if not order:
        raise errors.ToolExecutionError(f"Order {order_id} not found")
    details = {
        "order_id": order.id,
        "product": order.product_name,
        "amount": order.amount,
        "status": order.status,
        "refunded": order.refunded
    }
    logger.info(f"Fetched order details for {order_id}")
    return details
