from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # App
    APP_NAME: str = "AI Customer Support Agent"
    ENV: str = "dev"

    # LLM
    GEMINI_API_KEY: str | None = None
    LLM_MODEL: str = "gemini-1.5-pro"

    # Vector DB
    PINECONE_API_KEY: str | None = None
    PINECONE_INDEX_NAME: str = "support-policies"

    # Database
    DATABASE_URL: str = "sqlite:///./support.db"

    # Agent behavior
    CONFIDENCE_THRESHOLD: float = 0.65
    MAX_AGENT_STEPS: int = 5

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache
def get_settings() -> Settings:
    return Settings()
