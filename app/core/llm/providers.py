from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.language_models.chat_models import BaseChatModel
from app.config.llm import LLMSettings

def get_ollama(settings: LLMSettings) -> BaseChatModel:
    """Подключение к локальным моделям Ollama"""
    return ChatOllama(
        model=settings.model_name,
        temperature=settings.temperature,
        base_url=settings.ollama_base_url
    )

def get_openai(settings: LLMSettings) -> BaseChatModel:
    """Подключение к моделям, которые могут реализовывать OpenAI интерфейс"""
    return ChatOpenAI(
        model=settings.model_name,
        temperature=settings.temperature,
        api_key=settings.openai_api_key,
        base_url=settings.openai_url,
    )

PROVIDERS_MAP = {
    "openai": get_openai,
    "ollama": get_ollama
}