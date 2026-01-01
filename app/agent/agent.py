from app.services.llm import LLMClient
from app.agent.state import ConversationState
from app.agent.guardrails import check_confidence, enforce_max_steps, should_escalate
from app.services.logger import logger

class CustomerSupportAgent:
    """
    AI agent that orchestrates tools and LLM
    """

    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client

    def handle_query(self, user_id: int, query: str, tools: dict):
        """
        tools: dict of {"tool_name": callable}
        """
        state = ConversationState(user_id)
        step_count = 0

        while step_count < 5:
            enforce_max_steps(state)

            # Call LLM to decide next action
            prompt = f"{query}\nAvailable tools: {list(tools.keys())}"
            llm_response = self.llm.generate_text(prompt)
            logger.info(f"LLM response: {llm_response}")

            # Mock confidence (in production, parse from LLM)
            confidence = 0.9
            check_confidence(confidence)

            # Decide which tool to call (simple example: pick first tool mentioned)
            called_tool = None
            for tool_name in tools.keys():
                if tool_name.lower() in llm_response.lower():
                    called_tool = tool_name
                    break

            tool_success = True
            tool_output = None
            if called_tool:
                try:
                    tool_output = tools[called_tool]()
                except Exception as e:
                    logger.error(f"Tool {called_tool} failed: {e}")
                    tool_success = False

            # Check if escalation needed
            if should_escalate(confidence, tool_success):
                logger.info("Escalation required")
                state.add_step(
                    action="escalate",
                    tool=called_tool,
                    input_data={"query": query},
                    llm_output=llm_response
                )
                return {"escalate": True, "state": state.steps}

            # Log step
            state.add_step(
                action="tool_call" if called_tool else "llm_response",
                tool=called_tool,
                input_data={"query": query},
                llm_output=llm_response
            )

            # Break after first iteration for demo
            break

        return {"response": llm_response, "state": state.steps}
