from sentence_transformers import SentenceTransformer
import pinecone
from app.config import get_settings
from app.services.logger import logger

settings = get_settings()

class VectorStore:
    def __init__(self):
        # Load embedding model
        self.embed_model = SentenceTransformer("all-MiniLM-L6-v2")
        logger.info("Embedding model loaded")

        # Initialize Pinecone client
        self.pc = pinecone.Pinecone(api_key=settings.PINECONE_API_KEY)
        index_name = settings.PINECONE_INDEX_NAME
        if index_name not in self.pc.list_indexes().names():
            self.pc.create_index(
                name=index_name,
                dimension=384,  # dimension of MiniLM-L6-v2 embeddings
            )
        self.index = self.pc.Index(index_name)
        logger.info(f"Pinecone index ready: {index_name}")

    def upsert(self, vectors: list[dict]):
        """
        vectors = [{"id": str, "values": List[float], "metadata": dict}, ...]
        """
        if self.mock:
            logger.info(f"[MOCK VECTOR UPSERT] {len(vectors)} vectors")
            return
        self.index.upsert(vectors)

    def query(self, query_text: str, top_k: int = 3) -> list[str]:
        # 1️⃣ Encode query
        embedding = self.embed_model.encode([query_text])[0].tolist()
        # 2️⃣ Query Pinecone
        response = self.index.query(vector=embedding, top_k=top_k, include_metadata=True)
        # 3️⃣ Extract text from metadata
        return [match.metadata.get("text", match.id) for match in response.matches]
