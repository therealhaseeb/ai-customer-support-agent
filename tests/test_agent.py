from app.services.llm import LLMClient
from app.agent.agent import CustomerSupportAgent
from app.tools import order_tools, refund_tools, ticket_tools

# Mock DB tools for demo
db_tools = {
    "order_tool": lambda: order_tools.get_order_details(SessionLocal(), 1),
    "refund_tool": lambda: refund_tools.process_refund(SessionLocal(), 1),
    "ticket_tool": lambda: ticket_tools.create_support_ticket(SessionLocal(), 1, "Cannot login")
}

llm = LLMClient()
agent = CustomerSupportAgent(llm)

query = "Check my order status and process refund if eligible"
result = agent.handle_query(user_id=1, query=query, tools=db_tools)
print(result)
