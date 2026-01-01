import sys
import os

# Add project root to sys.path so 'app' can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.database import Base, engine, SessionLocal
from app.db import crud

# ------------------------
# Create tables
# ------------------------
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# ------------------------
# Create sample users
# ------------------------
user1 = crud.create_user(db, name="Alice", email="alice@example.com")
user2 = crud.create_user(db, name="Bob", email="bob@example.com")

# ------------------------
# Create sample orders
# ------------------------
order1 = crud.create_order(db, user1.id, "Laptop", 1200.0)
order2 = crud.create_order(db, user2.id, "Headphones", 200.0)

# Update order statuses
crud.update_order_status(db, order1.id, "delivered")
crud.update_order_status(db, order2.id, "pending")

# ------------------------
# Create sample tickets
# ------------------------
ticket1 = crud.create_ticket(db, user1.id, "Cannot login")
ticket2 = crud.create_ticket(db, user2.id, "Payment failed")

print("✅ Sample data setup complete")
