from src.configs import MAX_CONTEXT_CHARS


def summarize_history(history: list[dict], max_messages: int = 8) -> list[dict]:
    return history[-max_messages:]


def trim_context(context: str) -> str:
    return context[:MAX_CONTEXT_CHARS]
