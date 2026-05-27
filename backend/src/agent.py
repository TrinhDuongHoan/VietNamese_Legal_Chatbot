from __future__ import annotations

from src.legal_tools import (
    calculate_contract_penalty,
    calculate_inheritance_shares,
    check_legal_age,
)
from src.tavily_tool import web_search



def run_agent(question: str) -> str:
    text = question.lower()
    if "phạt" in text and "hợp đồng" in text:
        result = calculate_contract_penalty(100_000_000, 0.001, 30)
        return f"Kết quả tính phạt mẫu: {result}"
    if "đủ tuổi" in text or "bao nhiêu tuổi" in text:
        result = check_legal_age(2005)
        return f"Kết quả kiểm tra tuổi mẫu: {result}"
    if "thừa kế" in text or "chia di sản" in text:
        result = calculate_inheritance_shares(2, spouse=True, parents=0)
        return f"Kết quả chia thừa kế mẫu: {result}"
    if any(k in text for k in ["mới nhất", "hiện nay", "2025", "2026"]):
        results = web_search(question)
        if results:
            bullets = "\n".join(f"- {r.get('title')}: {r.get('url')}" for r in results[:5])
            return f"Kết quả web search:\n{bullets}"
    return "Hiện agent chưa cần dùng tool riêng cho câu hỏi này."
