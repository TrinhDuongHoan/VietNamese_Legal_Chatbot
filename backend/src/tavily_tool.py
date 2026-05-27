from __future__ import annotations

import requests

from src.configs import TAVILY_API_KEY



def web_search(query: str) -> list[dict]:
    if not TAVILY_API_KEY:
        return []
    resp = requests.post(
        "https://api.tavily.com/search",
        json={"api_key": TAVILY_API_KEY, "query": query, "search_depth": "basic", "max_results": 5},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json().get("results", [])
