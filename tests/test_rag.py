from app.rag.embeddings import Embeddings
from app.services.vector_store import VectorStore
from app.rag.ingest import PDFIngestor
from app.rag.retriever import Retriever

emb = Embeddings()
vs = VectorStore()
ingestor = PDFIngestor(emb, vs)
retriever = Retriever(emb, vs)

# Ingest PDF folder
ingestor.ingest_folder("data/policies")

# Test retrieval
query = "Refund policy for electronics"
docs = retriever.retrieve(query)
print(f"Retrieved {len(docs)} docs for query: '{query}'")
print(docs[0])
