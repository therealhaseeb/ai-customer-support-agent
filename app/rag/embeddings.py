from sentence_transformers import SentenceTransformer
from app.services.logger import logger

class Embeddings:
    """
    HuggingFace / SentenceTransformer embeddings
    """
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        logger.info(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)

    def embed_text(self, text: str) -> list[float]:
        return self.model.encode(text).tolist()

    def embed_documents(self, docs: list[str]) -> list[list[float]]:
        return self.model.encode(docs).tolist()
