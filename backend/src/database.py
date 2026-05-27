from celery import Celery
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.configs import DATABASE_URL, CELERY_BROKER_URL, CELERY_RESULT_BACKEND

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_celery_app(name: str) -> Celery:
    app = Celery(name, broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)
    app.conf.update(
        task_serializer="json",
        result_serializer="json",
        accept_content=["json"],
        timezone="Asia/Ho_Chi_Minh",
        enable_utc=True,
    )
    return app
