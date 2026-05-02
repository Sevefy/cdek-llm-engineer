from typing import Literal, Optional
from pydantic import BaseModel
import os
from pathlib import Path

class Document(BaseModel):
    """Модель документа"""
    name: str
    content: str
    category: Literal["general", "country"]
    country: Optional[Literal["germany", "france"]] = None
    
class DocumentStore:
    """Хранилище документов"""
    def __init__(self):
        self.documents: list[Document] = []
        
    def add_document(self, name: str, content: str, category: Literal["general", "country"], country: Optional[Literal["germany", "france"]] = None):
        """Добавление документа в хранилище"""
        doc = Document(name=name, content=content, category=category, country=country)
        self.documents.append(doc)
    
    def get_general_context(self) -> str:
        """Получение основной информации"""
        general_docs = list(filter(lambda doc: doc.category == "general", self.documents))
        return "\n".join(doc.content for doc in general_docs)
    
    def get_country_context(self, country: Literal["germany", "france"]) -> str:
        """Получение ифномрации по стране"""
        country_docs = list(filter(lambda doc: doc.category == "country" and doc.country == country, self.documents))
        return "\n".join(doc.content for doc in country_docs)
    
    def get_full_context(self, country: Literal["germany", "france"]) -> str:
        """Основа + страна"""
        parts = [self.get_general_context()]
        country_context = self.get_country_context(country)
        parts.append(country_context)
        return "\n".join(parts)

class LoadDocuments:
    """Загрузчик документов"""
    def __init__(self, path_docs: str):
        self.path = path_docs
        
    def load(self, store: DocumentStore):
        """Функция загрузки из директории в хранилище"""
        general_files = ["general_info.txt", "deadlines.txt", "benefits.txt"]
        country_files = ["france_rules.txt", "germany_rules.txt"]
        
        for filename in general_files:
            with open(Path(self.path, filename), encoding="utf-8") as file:
                text = file.read()
                store.add_document(filename, text, category="general")
                
        for filename in country_files:
            with open(Path(self.path, filename), encoding="utf-8") as file:
                text = file.read()
                country = self.get_country_by_filename(filename)
                store.add_document(filename, text, category="country", country=country)
                
        return store
    
    def get_country_by_filename(self, filename: str):
        match filename.split("_")[0]:
            case "france":
                return "france"
            case "germany":
                return "germany"
            case _:
                raise ValueError("Страна не обрабатывается")     
            
if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

    store = DocumentStore()
    
    loader = LoadDocuments(Path(base_dir, "data"))
    loader.load(store)
    
    print(store.get_country_context("germany"))
    print(store.get_full_context("france"))