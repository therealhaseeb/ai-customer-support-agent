from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.llm import LLMClient
from app.services.vector_store import VectorStore
from app.db import crud, database

router = APIRouter()

# ------------------------
# Request model
# ------------------------
class QueryRequest(BaseModel):
    user_id: int
    query: str

# ------------------------
# Initialize LLM and RAG
# ------------------------
llm = LLMClient()
vector_search = VectorStore()  # Make sure this works with your Pinecone VectorStore

# ------------------------
# /api/query endpoint
# ------------------------
@router.post("/query")
def query_agent(request: QueryRequest):
    # Validate user exists
    db = database.SessionLocal()
    user = crud.get_user(db, request.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # ------------------------
    # Step 1 — Retrieve relevant policy text using RAG
    # ------------------------
    docs = vector_search.query(request.query, top_k=3)  # returns list of text
    context_text = "\n".join(docs) if docs else "No relevant policy found."

    # ------------------------
    # Step 2 — Construct prompt for LLM
    # ------------------------
    prompt = f"""
You are an AI customer support agent.
User Question: {request.query}
Context / Policy Info: {context_text}

Answer concisely, and suggest refund eligibility if applicable.
"""

    # ------------------------
    # Step 3 — Get LLM response
    # ------------------------
    try:
        answer = llm.generate_text(prompt)
    except Exception as e:
        # In case LLM fails, escalate
        answer = f"Error generating answer: {str(e)}"
        return {
            "user_id": request.user_id,
            "query": request.query,
            "response": answer,
            "escalate": True,
            "tool_outputs": [],
            "conversation_state": []
        }

    # ------------------------
    # Step 4 — Return structured response
    # ------------------------
    return {
        "user_id": request.user_id,
        "query": request.query,
        "response": answer,
        "retrieved_docs": docs,
        "escalate": False,
        "tool_outputs": [],
        "conversation_state": []
    }
