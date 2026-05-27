from __future__ import annotations


def rewrite_followup_query(question: str, history: list[dict]) -> str:
    if not history:
        return question
    last_user = None
    for item in reversed(history):
        if item.get("role") == "user":
            last_user = item.get("content")
            break
    if not last_user or question.strip().lower() == last_user.strip().lower():
        return question
    if len(question.split()) < 6:
        return f"{last_user}. Câu hỏi tiếp theo: {question}"
    return question


def rewrite_query_to_multi_queries(question: str) -> list[str]:
    q = question.strip()
    return [q, f"quy định {q}", f"thủ tục {q}"]
