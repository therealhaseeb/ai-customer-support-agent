from typing import List
from google import genai
from app.config import get_settings
from app.services.logger import logger

settings = get_settings()

# -------------------------------------------------------------------
# Configure Gemini Client
# -------------------------------------------------------------------

def _init_gemini_client():
    """
    Initialize the Gemini client with your API key.
    Uses the google-generativeai library.
    """
    if not settings.GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is not set in .env")

    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    return client

# Initialize once
_gemini = _init_gemini_client()

# -------------------------------------------------------------------
# LLM Client Wrapper
# -------------------------------------------------------------------

class LLMClient:
    """
    Wrapper around Gemini model calls.
    """

    def __init__(self, model_name: str = None):
        self.model_name = model_name or settings.LLM_MODEL

    def generate_text(
        self,
        prompt: str,
        max_output_tokens: int = 512,
        temperature: float = 0.0,
    ) -> str:
        """
        Generate text from Gemini.
        """
        logger.info(f"LLM request to model={self.model_name}")

        response = _gemini.models.generate_content(
                            model="gemini-2.5-flash", 
                            contents="Explain how AI works in a few words")

        # The SDK may return multiple text segments
        # Join them (simple case)
        text = response.text if hasattr(response, "text") else ""
        logger.info("LLM response received")
        return text

    def chat(
        self,
        messages: List[dict],
        max_output_tokens: int = 512,
        temperature: float = 0.0,
    ) -> str:
        """
        Gemini-style chat with system + user messages.
        """
        logger.info(f"LLM chat to model={self.model_name}")

        # Prepend system messages if you want roles
        response = _gemini.models.generate_content(
            model=self.model_name,
            contents=messages,
            config={
                "temperature": temperature,
                "maxOutputTokens": max_output_tokens,
            },
        )

        # Extract response text
        text = response.text if hasattr(response, "text") else ""
        logger.info("LLM chat response received")
        return text