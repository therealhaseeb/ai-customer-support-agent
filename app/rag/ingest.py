import os
from pathlib import Path
from PyPDF2 import PdfReader
from app.rag.embeddings import Embeddings
from app.services.vector_store import VectorStore
from app.services.logger import logger

class PDFIngestor:
    def __init__(self, embeddings: Embeddings, vector_store: VectorStore):
        self.embeddings = embeddings
        self.vector_store = vector_store

    def load_pdfs(self, folder_path: str):
        folder = Path(folder_path)
        pdfs = list(folder.glob("*.pdf"))
        logger.info(f"Found {len(pdfs)} PDFs in {folder_path}")
        return pdfs

    def extract_text(self, pdf_path: Path) -> str:
        reader = PdfReader(str(pdf_path))
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text

    def chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50):
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            start += chunk_size - overlap
        return chunks

    def ingest_folder(self, folder_path: str):
        pdfs = self.load_pdfs(folder_path)
        for pdf in pdfs:
            text = self.extract_text(pdf)
            chunks = self.chunk_text(text)
            vectors = []
            for i, chunk in enumerate(chunks):
                embedding = self.embeddings.embed_text(chunk)
                vectors.append({"id": f"{pdf.stem}_{i}", "values": embedding, "metadata": {"text": chunk}})
            self.vector_store.upsert(vectors)
            logger.info(f"Ingested {len(chunks)} chunks from {pdf.name}")
