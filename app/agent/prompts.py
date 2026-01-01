# Prompts for LLM and tool guidance

SYSTEM_PROMPT = """
You are an AI Customer Support Agent.
You can:
- Answer user questions about orders, tickets, and policies.
- Call tools when necessary.
- Escalate to human if unsure.
- Respect company policies and guardrails.
"""

TOOL_PROMPT_TEMPLATE = """
Use the following tool if appropriate:

Tool Name: {tool_name}
Description: {description}
Input: {input_spec}
"""

def format_tool_prompt(tool_name: str, description: str, input_spec: str) -> str:
    return TOOL_PROMPT_TEMPLATE.format(
        tool_name=tool_name,
        description=description,
        input_spec=input_spec
    )
