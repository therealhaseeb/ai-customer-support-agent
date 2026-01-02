import sys
import os

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.rag.embeddings import Embeddings
from app.rag.ingest import PDFIngestor
from app.services.vector_store import VectorStore

# ------------------------
# Initialize embeddings and vector store
# ------------------------
emb = Embeddings()
vs = VectorStore()
ingestor = PDFIngestor(emb, vs)

# ------------------------
# Ingest PDFs from folder
# ------------------------
folder_path = "data/policies"

if not os.path.exists(folder_path):
    print(f"❌ Folder not found: {folder_path}")
    exit(1)

pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")]

if not pdf_files:
    print(f"❌ No PDFs found in {folder_path}")
    exit(1)

print(f"ℹ️ Found {len(pdf_files)} PDFs in {folder_path}")

for pdf_file in pdf_files:
    pdf_path = os.path.join(folder_path, pdf_file)
    ingestor.ingest_folder(pdf_path)
    print(f"✅ Ingested {pdf_file}")

print("✅ PDF ingestion complete")
