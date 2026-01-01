from typing import Optional


class AgentError(Exception):
    """
    Base class for all agent-related errors.
    """

    def __init__(self, message: str, details: Optional[dict] = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def __str__(self) -> str:
        return f"{self.message} | Details: {self.details}"


# =========================
# Tool & Execution Errors
# =========================

class ToolExecutionError(AgentError):
    """
    Raised when a tool (API / DB / function) fails.
    """
    pass


class ToolNotFoundError(AgentError):
    """
    Raised when the agent tries to call a non-registered tool.
    """
    pass


class ToolInputValidationError(AgentError):
    """
    Raised when tool arguments are invalid or incomplete.
    """
    pass


# =========================
# Policy & Decision Errors
# =========================

class PolicyConflictError(AgentError):
    """
    Raised when multiple policies contradict each other.
    """
    pass


class RefundNotAllowedError(AgentError):
    """
    Raised when refund conditions are not met.
    """
    pass


class UnauthorizedActionError(AgentError):
    """
    Raised when agent attempts a restricted action.
    """
    pass


# =========================
# Confidence & Safety
# =========================

class LowConfidenceError(AgentError):
    """
    Raised when LLM confidence is below acceptable threshold.
    """
    pass


class HallucinationDetectedError(AgentError):
    """
    Raised when response is not grounded in tools or RAG context.
    """
    pass


# =========================
# Escalation & Workflow
# =========================

class EscalationRequired(AgentError):
    """
    Raised when issue must be routed to a human agent.
    """
    pass


class MaxStepsExceededError(AgentError):
    """
    Raised when agent exceeds allowed reasoning steps.
    """
    pass


# =========================
# API / External Errors
# =========================

class ExternalServiceError(AgentError):
    """
    Raised when an external service (CRM, payment, etc.) fails.
    """
    pass
