from app.rag.embeddings import Embeddings
from app.services.vector_store import VectorStore
from app.services.logger import logger

class Retriever:
    def __init__(self, embeddings: Embeddings, vector_store: VectorStore):
        self.embeddings = embeddings
        self.vector_store = vector_store

    def retrieve(self, query: str, top_k: int = 5):
        query_vector = self.embeddings.embed_text(query)
        results = self.vector_store.query(query_vector, top_k=top_k)
        # Extract text from metadata
        docs = [match["metadata"]["text"] for match in results]
        logger.info(f"Retrieved {len(docs)} docs for query: {query}")
        return docs
