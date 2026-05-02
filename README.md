# Тестовое задание для стажера LLM Engineer

FastAPI-приложение с ИИ-агентом для ответов на вопросы по международной стажировке CDEK.

# Автор

Малофеев Арсений
arseniy.malofeev@bk.ru

## Основные функции

- Чат с ИИ-агентом на основе LLM (OpenAI или Ollama)
- Автоматическое определение страны по запросу
- Контекстное понимание на основе загруженных правил стажировки
- Сохранение сессий чата через cookies
- RESTful API через FastAPI

## API endpoints

Основной эндпоинт для взаимодействия с ИИ-агентом:

**POST /chat**
- Заголовок: `Content-Type: application/json`
- Тело запроса:
  ```json
  {
    "text": "Ваш вопрос"
  }
  ```
- Ответ:
  ```json
  {
    "response": "Ответ ИИ-агента",
    "country": "france/germany/null"
  }
  ```

## Установка и запуск

### Требования

- Python 3.11+
- Docker и Docker Compose

### Запуск через Docker

```bash
docker-compose up --build
```

Приложение будет доступно на `http://localhost:8000`

### Запуск локально

```bash
# Создание виртуального окружения
python -m venv .venv
source .venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt

# Запуск сервера
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
или
python -m app.main
```

## Настройка LLM

Приложение поддерживает два режима работы с языковой моделью:

### OpenAI (рекомендуется)

1. Получите API ключ модели, которая поддерживает OpenAI формат (для тестирования использовался LongCat https://longcat.chat/platform/docs/#endpoints)
2. Создайте файл `.env` в корне проекта:
```
LLM_PROVIDER=openai
LLM_MODEL_NAME=имя-модели
LLM_OPENAI_API_KEY=ключ
LLM_OPENAI_URL=url-модели
LLM_TEMPERATURE=0.0 # по умолчанию

```
### Ollama (альтернатива)

1. Разверните локально подходящую модель
2. В `.env` файле укажите:
```
LLM_PROVIDER=ollama # провайдер по умолчанию
LLM_MODEL_NAME=имя-модели # llama3.2:3b - по умолчанию
LLM_OLLAMA_BASE_URL="http://localhost:11434" # по умолчанию
LLM_TEMPERATURE=0.0 # по умолчанию
```

## Ограничения

- Максимальная длина вопроса: 4096 символов
- Требует API ключа OpenAI или локальной установки Ollama

## Разработка

### Структура проекта

```
cdek-llm-engineer/
├── app/                    # Основное приложение
│   ├── core/               # Бизнес-логика
│   │   ├── llm/           # LLM провайдеры и фабрики
│   │   └── document_store.py # Загрузка и хранение документов
│   ├── graph/             # LangGraph графы
│   │   ├── graph.py       # Главный граф чата
│   │   ├── nodes.py       # Узлы графа
│   │   └── state.py       # Состояние графа
│   ├── routes/            # API роутеры
│   │   └── chat.py        # Чат-эндпоинт
│   ├── schemas/           # Pydantic схемы
│   └── config/            # Конфигурация
├── data/                  # Данные правил стажировки
├── Dockerfile             # Docker конфиг
├── docker-compose.yml     # Docker Compose
└── requirements.txt       # Зависимости
```