from __future__ import annotations

import time

from celery.result import AsyncResult
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from src.database import get_db
from src.import_data import import_qa_data
from src.models import Document
from src.schemas import CompleteRequest, DocumentCreateRequest
from src.tasks import llm_handle_message

app = FastAPI(title="Vietnamese Legal Chatbot Backend")


@app.get("/health")
def health():
    return {"status": "healthy", "service": "Vietnamese Legal Chatbot Backend"}


@app.post("/document/create")
def create_document(payload: DocumentCreateRequest, db: Session = Depends(get_db)):
    row = Document(question=payload.question, content=payload.content)
    db.add(row)
    db.commit()
    db.refresh(row)
    return {"id": row.id, "question": row.question}


@app.post("/data/import")
def import_data():
    result = import_qa_data("/app/data/train.jsonl")
    return {"success": True, "result": result}


@app.post("/chat/complete")
def complete(data: CompleteRequest):
    if not data.user_id or not data.user_message:
        raise HTTPException(status_code=400, detail="user_id và user_message là bắt buộc")

    if data.sync_request:
        result = llm_handle_message(data.bot_id, data.user_id, data.user_message)
        return {"task_status": "SUCCESS", "task_result": result}

    task = llm_handle_message.delay(data.bot_id, data.user_id, data.user_message)
    return {"task_id": task.id}


@app.get("/chat/complete/{task_id}")
def get_response(task_id: str):
    start = time.time()
    while True:
        result = AsyncResult(task_id)
        if not result.ready():
            if time.time() - start > 120:
                return {
                    "task_id": task_id,
                    "task_status": result.status,
                    "error_message": "Yêu cầu đang xử lý quá lâu. Hãy thử lại sau.",
                }
            time.sleep(0.5)
            continue

        if result.successful():
            return {"task_id": task_id, "task_status": result.status, "task_result": result.result}

        return {
            "task_id": task_id,
            "task_status": result.status,
            "error_message": str(result.result or "Yêu cầu xử lý thất bại."),
        }
