from typing import Optional

from pydantic import BaseModel, Field

class ChatRequestSchema(BaseModel):
    text: str = Field(..., max_length=1024)

class ChatResponseSchema(BaseModel):
    response: str
    country: Optional[str]

    
    
