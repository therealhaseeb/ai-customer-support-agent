from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

# ------------------------
# Users
# ------------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    tickets = relationship("Ticket", back_populates="user")
    orders = relationship("Order", back_populates="user")


# ------------------------
# Orders
# ------------------------
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String, default="pending")  # pending, shipped, delivered
    refunded = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="orders")


# ------------------------
# Support Tickets
# ------------------------
class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    issue = Column(String, nullable=False)
    status = Column(String, default="open")  # open, resolved, escalated
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="tickets")
