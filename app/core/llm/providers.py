from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.language_models.chat_models import BaseChatModel
from app.config.llm import LLMSettings

def get_ollama(settings: LLMSettings) -> BaseChatModel:
    return ChatOllama(
        model=settings.model_name,
        temperature=settings.temperature,
        base_url=settings.ollama_base_url
    )

def get_openai(settings: LLMSettings) -> BaseChatModel:
    return ChatOpenAI(
        model=settings.model_name,
        temperature=settings.temperature,
        api_key=settings.open_api_key,
        base_url=settings.openai_url,
        max_retries=5
    )

PROVIDERS_MAP = {
    "openai": get_openai,
    "ollama": get_ollama
}