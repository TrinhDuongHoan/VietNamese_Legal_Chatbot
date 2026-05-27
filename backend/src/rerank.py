from __future__ import annotations

from typing import Any


def rerank_documents(query: str, documents: list[dict[str, Any]], limit: int = 5) -> list[dict[str, Any]]:
    terms = {t.lower() for t in query.split() if t.strip()}
    rescored = []
    for doc in documents:
        text = f"{doc.get('question', '')} {doc.get('content', '')}".lower()
        overlap = sum(1 for t in terms if t in text)
        score = doc.get("similarity_score", 0.0) + doc.get("lexical_score", 0.0) + overlap * 0.1
        rescored.append({**doc, "rerank_score": score})
    rescored.sort(key=lambda x: x["rerank_score"], reverse=True)
    return rescored[:limit]
