from app.config import get_settings
from app.utils import errors

settings = get_settings()

def check_confidence(confidence: float):
    if confidence < settings.CONFIDENCE_THRESHOLD:
        raise errors.LowConfidenceError(
            f"Confidence {confidence:.2f} below threshold {settings.CONFIDENCE_THRESHOLD}"
        )

def enforce_max_steps(agent_state):
    if len(agent_state.steps) >= settings.MAX_AGENT_STEPS:
        raise errors.MaxStepsExceededError("Agent exceeded maximum reasoning steps")

def should_escalate(llm_confidence: float, tool_success: bool):
    """
    Determine if escalation to human is required
    """
    if not tool_success or llm_confidence < settings.CONFIDENCE_THRESHOLD:
        return True
    return False
