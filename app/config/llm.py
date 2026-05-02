from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal, Optional

class LLMSettings(BaseSettings):
    """Конфигурация LLM"""
    model_config = SettingsConfigDict(
        env_prefix="LLM_",
        env_file=".env",
        extra="ignore"
    )
    
    provider: Literal["ollama", "openai"] = "ollama"
    
    model_name: str = "llama3.2:3b"
    temperature: float = 0.0
    
    openai_api_key: Optional[str] = None
    ollama_base_url: str = "http://localhost:11434"
    
    openai_url: Optional[str] = "https://api.longcat.chat/openai"