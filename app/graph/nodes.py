from langchain_core.exceptions import OutputParserException

from app.core import document_store
from app.graph.state import ChatState
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage

from app.schemas.llm import RouteDecision
from langchain_core.language_models import BaseChatModel
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),                    # максимум 3 попытки
    wait=wait_exponential(multiplier=1, min=1, max=4),  # экспоненциальная задержка
    retry=retry_if_exception_type((OutputParserException, Exception)),
    reraise=True
)
async def route_message(llm: BaseChatModel, messages: list[BaseMessage] | BaseMessage) -> RouteDecision:
    """Извлечение инфомации о пользователе исходя из контекста"""
    system_prompt = """Ты — роутер чат-бота программы международной стажировки.
Твоя задача — анализировать ВСЕ предыдущие сообщения и текущее сообщение пользователя. 
Если у тебя уже есть информация о стране и статусе студента из предыдущих сообщений — просто верни JSON с этими данными, needs_clarification=false.
Определи страну в которой пользователь собирается проходить стажировку.
ВСЕГДА указывай почему ты принял такое решение в поле reasoning

Анализируй сообщение пользователя.
Отвечай **строго** в формате JSON. Никакого другого текста быть не должно.

{
  "reasoning": "короткое объяснение",
  "detected_country": "germany" или "france" или null,
  "detected_student": true/false/null,
  "needs_clarification": true/false,
  "clarification_question": "вопрос или null",
  "can_answer": true/false
}

Правила:
- Если пользователь явно указывает Германию/Germany/Берлин, то detected_country = "germany"
- Если пользователь явно указывает Францию/France/Париж, то detected_country = "france"
- Если страна не указана явно, то needs_clarification = true и заполни clarification_question
- Если needs_clarification = true, то добавь в clarification_question что стажировка может быть только во Франции и Германии
- Если ты смог определить страну, запиши ее в detected_country: france, germany, null
- Если пользователь явно указывает что он студент последнего курса, то detected_student=True
- Если пользователь явно указывает что он не студент, то detected_student=False
- Если невозможно определить является пользователь студентом или нет, то needs_clarification = true и заполни clarification_question
- Если в clarification_question вопрос является ли пользователь студентом, то укажи в вопросе, что стажировка только для студентов последних курсов
- Обязательно заполни поля: reasoning, needs_clarification
- Отвечай **только** валидным JSON согласно схеме.
"""

    structured_llm = llm.with_structured_output(RouteDecision, method="json_schema")

    messages = [SystemMessage(content=system_prompt)] + messages if isinstance(messages, list) else [messages]

    result = await structured_llm.ainvoke(messages)
    return result

        
        
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
        *state.messages[-5:]   # последние 5 сообщений для контекста диалога
    ]

    response = await llm.ainvoke(messages)

    return {
        "messages": [response],
        "context": context 
    }