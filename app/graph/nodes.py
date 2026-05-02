
from app.graph.state import ChatState
from langchain_core.messages import SystemMessage, BaseMessage

from app.schemas.llm import RouteDecision
from langchain_core.language_models import BaseChatModel

async def route_message(llm: BaseChatModel, messages: list[BaseMessage] | BaseMessage) -> RouteDecision:
    """Извлечение инфомации о пользователе исходя из контекста"""
    system_prompt = """Ты — точный JSON-роутер для чат-бота стажировки CdekStart.

Твоя единственная задача — анализировать историю диалога и текущее сообщение пользователя, после чего вернуть **строго валидный JSON**.

Никогда не пиши ничего кроме JSON. Никаких объяснений, никакого markdown.

{
  "reasoning": "короткое объяснение твоего решения",
  "detected_country": "germany" или "france" или null,
  "detected_student": true или false или null,
  "needs_clarification": true или false,
  "clarification_question": "вопрос пользователю или null",
  "can_answer": true или false
}

Ключевые правила:
- Если пользователь явно называет страну (Германия, Germany, Франция, France, Берлин, Париж и т.п.) — установи detected_country.
- Если пользователь меняет страну — обнови detected_country.
- Если пользователь говорит, что он студент последнего курса — detected_student = true.
- Если говорит, что не студент — detected_student = false.
- Если информации достаточно для ответа — needs_clarification = false и can_answer = true.
- Если нужно уточнить страну или статус студента — needs_clarification = true и напиши понятный clarification_question.

Отвечай **только JSON**. Даже если ты уверен — всё равно верни JSON.
"""

    if isinstance(messages, BaseMessage):
        messages = [messages]
    full_messages = [SystemMessage(content=system_prompt)] + messages
    
    structured_llm = llm.with_structured_output(RouteDecision, method="json_schema", include_raw=True)
    raw_result = await structured_llm.ainvoke(full_messages)
    if raw_result.get('parsing_error'):
        raw_text = getattr(raw_result['raw'], 'content', str(raw_result['raw']))
        raise Exception(f"RAW_RESPONSE:{raw_text}")

    return raw_result['parsed']


        
        
async def answer_message(llm: BaseChatModel, state: ChatState) -> dict:
    """Генерация ответа по документам"""
    from app.core import doc_store
    country = state.detected_country
    
    # Получаем релевантный контекст
    context = doc_store.get_full_context(country)

    system_prompt = f"""Ты — консультант программы международной стажировки CdekStart.

Используй ТОЛЬКО следующую информацию для ответа. Не выдумывай ничего сверх этого.

{context}

Отвечай естественно, но строго на основе предоставленных данных.
Если информации недостаточно — честно скажи об этом."""

    messages = [
        SystemMessage(content=system_prompt),
        *state.messages[-20:]   # последние 20 сообщений для контекста диалога
    ]

    response = await llm.ainvoke(messages)

    return {
        "messages": [response],
        "context": context 
    }