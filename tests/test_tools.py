from app.db.database import SessionLocal
from app.tools import order_tools, refund_tools, ticket_tools
from app.rag.embeddings import Embeddings
from app.services.vector_store import VectorStore
from app.rag.retriever import Retriever
from app.tools.policy_tools import query_policy

db = SessionLocal()

# --- Test Orders ---
print(order_tools.get_order_status(db, 1))
print(order_tools.get_order_details(db, 1))

# --- Test Refund ---
try:
    print(refund_tools.process_refund(db, 1))
except Exception as e:
    print(e)

# --- Test Tickets ---
print(ticket_tools.create_support_ticket(db, 1, "Cannot login"))

# --- Test Policy Retrieval ---
emb = Embeddings()
vs = VectorStore()
retriever = Retriever(emb, vs)
policy = query_policy(retriever, "Refund policy for electronics")
print(policy)
