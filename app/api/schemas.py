from pydantic import BaseModel
from typing import Optional, Dict, List

# -----------------------------
# Request Models
# -----------------------------
class QueryRequest(BaseModel):
    user_id: int
    query: str

# Optional: tool outputs
class ToolOutput(BaseModel):
    tool: str
    result: Optional[Dict] = None

# -----------------------------
# Response Models
# -----------------------------
class QueryResponse(BaseModel):
    response: Optional[str] = None
    escalate: Optional[bool] = False
    tool_outputs: Optional[List[ToolOutput]] = []
    conversation_state: Optional[List[Dict]] = []
