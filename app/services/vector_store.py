import pinecone
from app.config import get_settings
from app.services.logger import logger

settings = get_settings()

class VectorStore:
    def __init__(self):
        if not settings.PINECONE_API_KEY:
            logger.warning("PINECONE_API_KEY not set. VectorStore will be mocked.")
            self.mock = True
        else:
            pinecone.init(api_key=settings.PINECONE_API_KEY, environment="us-west1-gcp")
            self.index = pinecone.Index(settings.PINECONE_INDEX_NAME)
            self.mock = False

    def upsert(self, vectors: list[dict]):
        """
        vectors = [{"id": str, "values": List[float], "metadata": dict}, ...]
        """
        if self.mock:
            logger.info(f"[MOCK VECTOR UPSERT] {len(vectors)} vectors")
            return
        self.index.upsert(vectors)

    def query(self, embedding: list[float], top_k: int = 5):
        if self.mock:
            logger.info(f"[MOCK VECTOR QUERY] top_k={top_k}")
            return [{"id": "mock_doc", "score": 0.9, "metadata": {"text": "Sample policy"}}]
        result = self.index.query(vector=embedding, top_k=top_k, include_metadata=True)
        return result["matches"]
