from pydantic import BaseModel, Field
from typing import Literal, Optional

class RouteDecision(BaseModel):
    """Схема роутера, полученный ответ в route_node от модели"""
    reasoning: str = Field(
        None, 
        description="Краткое объяснение, почему ты принял такое решение"
    )
    detected_country: Optional[Literal["germany", "france"]] = Field(
        None, 
        description="Страна пользователя: 'germany' или 'france'. Если не уверен — null"
    )
    detected_student: Optional[bool] = Field(
        None,
        description="Пользователь - студеет последнего курса или нет. True - студент последнего курса. False - не студент последнего курса"
    )
    needs_clarification: bool = Field(
        False, 
        description="True, если нужно задать уточняющий вопрос про страну или является ли он студентом"
    )
    clarification_question: Optional[str] = Field(
        None, 
        description="Вопрос пользователю, если needs_clarification=true"
    )
    can_answer: bool = Field(
        True, 
        description="Можно ли уже ответить на вопрос"
    )