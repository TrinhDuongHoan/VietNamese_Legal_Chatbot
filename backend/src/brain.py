from __future__ import annotations

from typing import Any

from langchain_core.messages import AIMessage, BaseMessage, ChatMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from src.configs import BASE_URL, MODEL_API_BASE, NO_THINK, OPENAI_API_KEY, TEMPERATURE
from src.query_rewriter import rewrite_followup_query
from src.rerank import rerank_documents
from src.search import hybrid_search
from src.summarizer import summarize_history, trim_context


client_kwargs = {
    "model": MODEL_API_BASE,
    "temperature": TEMPERATURE,
    "openai_api_key": OPENAI_API_KEY,
    "model_kwargs": NO_THINK,
}
if BASE_URL:
    client_kwargs["base_url"] = BASE_URL

client = (
    ChatOpenAI(**client_kwargs)
    if OPENAI_API_KEY
    else None
)


def _stringify_content(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
                continue
            if isinstance(block, dict):
                text = block.get("text")
                if isinstance(text, str):
                    parts.append(text)
        return "\n".join(part for part in parts if part)
    return str(content or "")


def _to_langchain_messages(messages: list[dict]) -> list[BaseMessage]:
    converted: list[BaseMessage] = []
    for message in messages:
        role = message.get("role", "user")
        content = _stringify_content(message.get("content", ""))

        if role == "system":
            converted.append(SystemMessage(content=content))
        elif role == "assistant":
            converted.append(AIMessage(content=content))
        elif role == "user":
            converted.append(HumanMessage(content=content))
        else:
            converted.append(ChatMessage(role=role, content=content))
    return converted


def detect_user_intent(question: str) -> str:
    text = question.lower()
    if any(k in text for k in ["phạt", "đủ tuổi", "thừa kế", "tính toán"]):
        return "agent_tools"
    if any(k in text for k in ["mới nhất", "hiện nay", "2025", "2026"]):
        return "web_search"
    if any(k in text for k in ["xin chào", "hello", "cảm ơn"]):
        return "general_chat"
    return "legal_rag"


def build_legal_rag_prompt(history: list[dict], question: str, documents: list[dict]) -> list[dict]:
    history = summarize_history(history)
    context = "\n\n".join(
        f"Câu hỏi: {d.get('question', '')}\nNội dung: {d.get('content', '')}" for d in documents
    )
    context = trim_context(context)
    system = {
        "role": "system",
        "content": (
            "Bạn là trợ lý pháp luật Việt Nam. Hãy trả lời rõ ràng, trung thực, bằng tiếng Việt. "
            "Nếu thiếu dữ liệu, hãy nói rõ giới hạn."
        ),
    }
    user = {
        "role": "user",
        "content": f"Tài liệu tham khảo:\n{context}\n\nCâu hỏi: {question}",
    }
    return [system] + history + [user]


def call_chat_model(messages: list[dict]) -> str:
    if not client:
        return (
            "Bạn chưa cấu hình OPENAI_API_KEY. Hệ thống hiện chạy ở chế độ fallback. "
            "Hãy thêm API key để nhận câu trả lời từ mô hình chat."
        )
    try:
        response = client.invoke(_to_langchain_messages(messages))
    except Exception as exc:
        return (
            "Không thể gọi mô hình chat. Hãy kiểm tra OPENAI_API_KEY, BASE_URL và MODEL_API_BASE. "
            f"Chi tiết: {exc}"
        )
    return _stringify_content(response.content)


def answer_general_chat(history: list[dict], question: str) -> str:
    messages = [{"role": "system", "content": "Bạn là trợ lý thân thiện, trả lời ngắn gọn."}] + history + [
        {"role": "user", "content": question}
    ]
    return call_chat_model(messages)


def answer_legal_rag(history: list[dict], question: str) -> str:
    standalone_question = rewrite_followup_query(question, history)
    docs = hybrid_search(standalone_question, limit=8)
    docs = rerank_documents(standalone_question, docs, limit=5)
    messages = build_legal_rag_prompt(history, standalone_question, docs)
    return call_chat_model(messages)
