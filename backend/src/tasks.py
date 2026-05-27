from __future__ import annotations

from src.agent import run_agent
from src.brain import answer_general_chat, answer_legal_rag, detect_user_intent
from src.database import SessionLocal, get_celery_app
from src.models import ChatConversation

celery_app = get_celery_app(__name__)



def save_message(bot_id: str, user_id: str, conversation_id: str, message: str, is_request: bool) -> None:
    db = SessionLocal()
    try:
        row = ChatConversation(
            conversation_id=conversation_id,
            bot_id=bot_id,
            user_id=user_id,
            message=message,
            is_request=is_request,
            completed=not is_request,
        )
        db.add(row)
        db.commit()
    finally:
        db.close()



def load_history(conversation_id: str) -> list[dict]:
    db = SessionLocal()
    try:
        rows = (
            db.query(ChatConversation)
            .filter(ChatConversation.conversation_id == conversation_id)
            .order_by(ChatConversation.created_at.asc())
            .all()
        )
        history = []
        for row in rows:
            history.append({
                "role": "user" if row.is_request else "assistant",
                "content": row.message or "",
            })
        return history
    finally:
        db.close()


@celery_app.task
def llm_handle_message(bot_id: str, user_id: str, question: str):
    conversation_id = f"{bot_id}:{user_id}"
    save_message(bot_id, user_id, conversation_id, question, True)
    history = load_history(conversation_id)
    route = detect_user_intent(question)

    if route == "legal_rag":
        answer = answer_legal_rag(history, question)
    elif route in {"agent_tools", "web_search"}:
        answer = run_agent(question)
    else:
        answer = answer_general_chat(history, question)

    save_message(bot_id, user_id, conversation_id, answer, False)
    return {"role": "assistant", "content": answer, "route": route}
