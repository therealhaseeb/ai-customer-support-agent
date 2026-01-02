import os
import sys
import time
import threading
import requests

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# ------------------------
# Step 1 — Load settings
# ------------------------
from app.config import get_settings
settings = get_settings()
print("✅ Loaded API keys from .env")

# ------------------------
# Step 2 — Setup DB + sample data
# ------------------------
from app.db.database import Base, engine, SessionLocal
from app.db import crud

Base.metadata.create_all(bind=engine)
db = SessionLocal()

user1 = crud.create_user(db, name="Alice", email="alice@example.com")
user2 = crud.create_user(db, name="Bob", email="bob@example.com")

order1 = crud.create_order(db, user1.id, "Laptop", 1200.0)
order2 = crud.create_order(db, user2.id, "Headphones", 200.0)

crud.update_order_status(db, order1.id, "delivered")
crud.update_order_status(db, order2.id, "pending")

crud.create_ticket(db, user1.id, "Cannot login")
crud.create_ticket(db, user2.id, "Payment failed")

print("✅ Sample data setup complete")

# ------------------------
# Step 3 — Create refund_policy.pdf
# ------------------------
from fpdf import FPDF

pdf_folder = "data/policies"
os.makedirs(pdf_folder, exist_ok=True)
pdf_file = os.path.join(pdf_folder, "refund_policy.pdf")

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.multi_cell(0, 10, """Refund Policy

1. Customers can request a refund within 30 days of delivery.
2. Orders must be in original condition.
3. Digital products are non-refundable.
4. Refunds will be processed within 5-7 business days.
5. For electronics, ensure all accessories and packaging are returned.

Thank you for shopping with us!
""")

pdf.output(pdf_file)

print(f"✅ Created sample PDF: {pdf_file}")

# ------------------------
# Step 4 — Ingest PDFs into vector store
# ------------------------
from app.rag.embeddings import Embeddings
from app.rag.ingest import PDFIngestor
from app.services.vector_store import VectorStore

emb = Embeddings()
vs = VectorStore()
ingestor = PDFIngestor(emb, vs)

ingestor.ingest_folder(pdf_folder)
print("✅ PDF ingestion complete")

# ------------------------
# Step 5 — Start FastAPI in a separate thread
# ------------------------
import subprocess
uvicorn_process = subprocess.Popen(
    ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

print("⌛ Waiting 3 seconds for FastAPI server to start...")
time.sleep(3)

# ------------------------
# Step 6 — Send a test query to the agent
# ------------------------
query = {
    "user_id": 1,
    "query": "Check my order status and refund eligibility"
}

try:
    response = requests.post("https://fuzzy-yodel-x4xwp9647pq3px4-8000.app.github.dev//query", json=query)
    print("✅ Sample query sent!")
    print("Response from AI Agent:")
    print(response.json())
except Exception as e:
    print(f"❌ Failed to query AI agent: {e}")

# ------------------------
# Done
# ------------------------
print("🎉 Demo complete! FastAPI server is running on http://127.0.0.1:8000")
print("You can send more queries via curl, Postman, or browser.")
