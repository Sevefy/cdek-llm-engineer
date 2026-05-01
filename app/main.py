from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn
from app.core.document_store import LoadDocuments
from app.routes import chat
from app.core import doc_store

@asynccontextmanager
async def lifespan(app: FastAPI):        
    loader = LoadDocuments("data")
    loader.load(doc_store)
    yield

app = FastAPI(
    debug=True,
    title="CDEK Chat",
    description="Тестовое задание на LLM-инженера",
    version="0.0.1",
    lifespan=lifespan
)

app.include_router(chat.router)


if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)
