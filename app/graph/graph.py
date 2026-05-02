from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage
from langgraph.graph import StateGraph, START, END

from app.core.llm.factory import get_llm
from app.schemas.llm import RouteDecision
from .state import ChatState
from app.graph.nodes import answer_message, route_message
from app.core.llm import settings_llm
from langgraph.checkpoint.memory import MemorySaver

llm:BaseChatModel = get_llm(settings_llm)

async def router_node(state: ChatState):
    """Главный узел, для определения информации об пользователе"""
    # if state.detected_student and state.detected_country:
    #     return {
    #         "next_step": "answer"
    #     } 
    
    last_message = state.messages[-1] if state.messages else ""
    
    if isinstance(last_message, AIMessage):
        return {
        }
        
    recent_messages = state.messages[-20:]
    try:
        decision = await route_message(llm, recent_messages)
        
        return {
            "detected_country": decision.detected_country,
            "detected_student": decision.detected_student,
            "needs_clarification": decision.needs_clarification,
            "clarification_question": decision.clarification_question,
        }
    except Exception as e:
        print(f"Router failed: {e}")
        if state.detected_country:
            return {
                "needs_clarification": False,
            }
        else:
            return {
                "needs_clarification": True,
                "clarification_question": "В какой стране вы планируете проходить стажировку? Германия или Франция?",
            }

async def clarification_node(state: ChatState):
    """Узел для уточнения"""
    return {
        "messages": [AIMessage(content=state.clarification_question)],
        "needs_clarification": True,
    }
    
async def answer_node(state: ChatState):
    """Узел генерации окончательного ответа по пользователю"""
    result = await answer_message(llm, state)
    return result

def init_nodes(graph: StateGraph):
    """Добавление узлов в граф"""
    graph.add_node("router", router_node)
    graph.add_node("clarify", clarification_node)
    graph.add_node("answer", answer_node)

def init_edges(graph: StateGraph):
    """Добавление граней между узлами в графе"""
    graph.add_edge(START, "router")
    graph.add_edge("clarify", END)
    graph.add_edge("answer", END)

def init_conditional_edges(graph: StateGraph):
    """Добавление условных узлов и переходов"""
    graph.add_conditional_edges(
        "router",
        lambda state: "clarify" if state.needs_clarification else "answer",
        {"clarify": "clarify", "answer": "answer"}
    )
    
def gen_png_graph(app_obj, name_photo: str = "graph.png") -> None:
    """
    Генерирует PNG-изображение графа и сохраняет его в файл.
    
    Args:
        app_obj: Скомпилированный объект графа
        name_photo: Имя файла для сохранения (по умолчанию "graph.png")
    """
    with open(name_photo, "wb") as f:
        f.write(app_obj.get_graph().draw_mermaid_png())
    
def build_graph():
    """Создание графа с memory"""
    graph = StateGraph(ChatState)
    init_nodes(graph)
    init_edges(graph)
    init_conditional_edges(graph)
    checkpointer = MemorySaver()
    app = graph.compile(checkpointer=checkpointer)
    
    gen_png_graph(app, name_photo="cdek_helper.png")
    return app
