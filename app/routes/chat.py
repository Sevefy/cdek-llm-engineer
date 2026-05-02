from fastapi import APIRouter, Depends, Request, Response
from app.graph.graph import build_graph
from app.graph.state import ChatState
from app.schemas.chat import ChatRequestSchema, ChatResponseSchema
from langchain_core.messages import HumanMessage
import secrets
router = APIRouter(prefix="/chat", tags=["Чат"])

chat_graph = build_graph()

def get_thread_id(request: Request, response: Response) -> str:
    """получение уникального thread_id"""
    coockie_thread = request.cookies.get("thread_id")
    if coockie_thread:
        return coockie_thread
    secret = secrets.token_hex(16)
    response.set_cookie("thread_id", secret)
    return secret

@router.post("", summary="\"ручка\" чата с ИИ-агентом")
async def chat(data: ChatRequestSchema, thread_id: str = Depends(get_thread_id)) -> ChatResponseSchema:
    config = {"configurable": {"thread_id": thread_id}}

    input_data = {
        "messages": [HumanMessage(content=data.text)]
    }

    try:
        result = await chat_graph.ainvoke(input_data, config=config)
    except Exception as e:
        print("Graph error:", e)
        return {"error": str(e)}

    ai_response = result["messages"][-1].content
    country =  result.get("detected_country")
    return ChatResponseSchema(response=ai_response, country=country)