from langchain_core.language_models import BaseChatModel

from app.config.llm import LLMSettings
from app.core.llm.providers import PROVIDERS_MAP


def get_llm(settings: LLMSettings) -> BaseChatModel:
    """Создание модели исходя из настроек"""
    provider = settings.provider
    if provider not in PROVIDERS_MAP:
        raise ValueError("Модель не поддерживается")
    return PROVIDERS_MAP[provider](settings)


    