import os

MYSQL_USER = os.getenv("MYSQL_USER", "legal_user")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "legal_pass")
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_DB = os.getenv("MYSQL_DB", "legal_chatbot")

DATABASE_URL = (
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@"
    f"{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
)

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
DEFAULT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION", "llm")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
MODEL_API_BASE = os.getenv("MODEL_API_BASE", os.getenv("OPENAI_MODEL", "Qwen/Qwen3.5-27B"))
OPENAI_MODEL = MODEL_API_BASE
BASE_URL = os.getenv("BASE_URL", os.getenv("OPENAI_BASE_URL", "")).strip()
TEMPERATURE = float(os.getenv("TEMPERATURE", "0"))
NO_THINK = {"extra_body": {"chat_template_kwargs": {"enable_thinking": False}}}
COHERE_API_KEY = os.getenv("COHERE_API_KEY", "")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")
EMBEDDING_MODEL_NAME = os.getenv(
    "EMBEDDING_MODEL_NAME",
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
)
MAX_CONTEXT_CHARS = int(os.getenv("MAX_CONTEXT_CHARS", "8000"))
