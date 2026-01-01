from app.rag.retriever import Retriever
from app.services.logger import logger

def query_policy(retriever: Retriever, question: str, top_k: int = 3):
    """
    Retrieve policy context for a given question
    """
    docs = retriever.retrieve(question, top_k=top_k)
    if not docs:
        logger.warning(f"No policy found for question: {question}")
        return "Policy information not found."
    logger.info(f"Retrieved {len(docs)} policy docs for question")
    return "\n".join(docs)
