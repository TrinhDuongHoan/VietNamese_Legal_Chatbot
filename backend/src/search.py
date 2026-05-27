from __future__ import annotations

from collections import Counter
from typing import Any

from src.custom_embedding import get_embedding
from src.vectorize import search_vectors

SEARCH_INDEX: list[dict[str, Any]] = []


def initialize_search_index(documents: list[dict[str, Any]]) -> None:
    global SEARCH_INDEX
    SEARCH_INDEX = documents[:]



def lexical_search(query: str, limit: int = 5) -> list[dict[str, Any]]:
    terms = [t.lower() for t in query.split() if t.strip()]
    scored = []
    for doc in SEARCH_INDEX:
        text = f"{doc.get('question', '')} {doc.get('content', '')}".lower()
        score = sum(text.count(t) for t in terms)
        if score > 0:
            scored.append({**doc, "lexical_score": float(score)})
    scored.sort(key=lambda x: x["lexical_score"], reverse=True)
    return scored[:limit]



def expand_queries(query: str) -> list[str]:
    q = query.strip()
    return [q, f"quy định pháp luật về {q}", f"theo luật Việt Nam {q}"]



def hybrid_search(query: str, limit: int = 5) -> list[dict[str, Any]]:
    merged: list[dict[str, Any]] = []
    seen = set()
    for q in expand_queries(query):
        vec_hits = search_vectors(get_embedding(q), limit=limit)
        lex_hits = lexical_search(q, limit=limit)
        for doc in vec_hits + lex_hits:
            key = (doc.get("question", ""), doc.get("content", ""))
            if key in seen:
                continue
            seen.add(key)
            merged.append(doc)
    merged.sort(
        key=lambda x: (x.get("similarity_score", 0.0) + x.get("lexical_score", 0.0)),
        reverse=True,
    )
    return merged[:limit]
