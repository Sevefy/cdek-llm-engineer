from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

from pydantic import BaseModel
from typing import Annotated, Literal, Optional

class ChatState(BaseModel):
    """Состояние пользователя в чате"""
    messages: Annotated[list[BaseMessage], add_messages]
    
    detected_country: Optional[Literal['germany', 'france']] = None
    detected_student: Optional[bool] = None
    needs_clarification: bool = False
    clarification_question: Optional[str] = None
    
    context: Optional[str] = None
    next_step: Optional[str] = None
    session_id: str = "default"
    
    