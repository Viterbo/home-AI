import os

class Settings:
    """Centralized configuration values."""
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://redis:6379/0")
    WORKSPACE_ROOT: str = os.getenv("WORKSPACE_ROOT", "/workspace")

settings = Settings()
