from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import schemas
from app.db.database import get_db
from app.services.llm import LLMClient
from app.agent.agent import CustomerSupportAgent
from app.services.logger import logger

router = APIRouter()

# Mock tools dictionary (replace with real tool calls)
def mock_order_tool():
    return {"order_id": 1, "status": "shipped"}

def mock_refund_tool():
    return {"order_id": 1, "refunded": True}

TOOLS = {
    "order_tool": mock_order_tool,
    "refund_tool": mock_refund_tool
}

# Instantiate LLM and agent
llm = LLMClient()
agent = CustomerSupportAgent(llm)


@router.post("/query", response_model=schemas.QueryResponse)
def handle_query(request: schemas.QueryRequest, db: Session = Depends(get_db)):
    """
    Endpoint to send user queries to AI agent.
    """
    try:
        result = agent.handle_query(user_id=request.user_id, query=request.query, tools=TOOLS)
        # Convert tool outputs
        tool_outputs = []
        for step in result["state"]:
            if step["tool"]:
                tool_outputs.append(schemas.ToolOutput(tool=step["tool"], result=step.get("input")))
        return schemas.QueryResponse(
            response=result.get("response"),
            escalate=result.get("escalate", False),
            tool_outputs=tool_outputs,
            conversation_state=result["state"]
        )
    except Exception as e:
        logger.error(f"Agent API error: {e}")
        return schemas.QueryResponse(response=str(e), escalate=True)
