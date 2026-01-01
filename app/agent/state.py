from typing import List, Dict

class ConversationState:
    """
    Tracks conversation steps, tool calls, and LLM outputs
    """
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.steps: List[Dict] = []

    def add_step(self, action: str, tool: str = None, input_data: dict = None, llm_output: str = None):
        step = {
            "action": action,
            "tool": tool,
            "input": input_data,
            "llm_output": llm_output
        }
        self.steps.append(step)

    def last_step(self):
        return self.steps[-1] if self.steps else None

    def reset(self):
        self.steps = []
